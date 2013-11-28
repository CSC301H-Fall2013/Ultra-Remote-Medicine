from sample.forms import NewCaseForm, UpdateCasePriorityForm, PostCommentForm, \
    UpdateCaseLockHolderForm, UpdateCaseStatusForm
from sample.models import Patient, Comment, Case, CommentGroup
from django.utils import timezone
from django.db import IntegrityError
from django.shortcuts import render_to_response
from django.template import RequestContext
from utilities import create_case_attributes, BoxedInteger, \
    create_comment_group_entries
from django.http import HttpResponseRedirect, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse


@login_required
def display_new_case(request, patient_id):
    ''' Display the new case page and process submitted new-case
        forms. patient_id specifies the default patient the case is for. Set
        to "X" if no patient is selected. '''

    user = request.user
    worker = request.user.worker

    if request.method == 'POST':

        form = NewCaseForm(request.POST)
        if form.is_valid():

            patient_id = form.cleaned_data['patient']
            comments = form.cleaned_data['comments']
            priority = form.cleaned_data['priority']

            try:
                patient = Patient.objects.filter(id=patient_id)[0]

                comment = Comment(
                    author=user,
                    text=comments,
                    time_posted=timezone.now())
                comment.save()

                comment_group = CommentGroup()
                comment_group.save()
                comment_group.comments.add(comment)

                case = Case(
                    patient=patient,
                    submitter_comments=comment_group,
                    priority=priority,
                    status=1,
                    submitter=worker,
                    date_opened=timezone.now())
                case.save()
            except IntegrityError, e:
                print str(e)
                print "hard fail"
                return HttpResponseServerError()

            return HttpResponseRedirect("/case/" + str(case.id))
    else:

        # The page has just been entered and so the form hasn't
        # been submitted yet.
        form = NewCaseForm()
        form.populate(patient_id)

    return render_to_response('newcase.html',
                              {'form': form,
                               'viewer': user},
                              context_instance=RequestContext(request))


@login_required
def display_case_list(request):
    ''' Displays the list of cases.'''

    user = request.user

    case_attributes = create_case_attributes(Case.objects)

    return render_to_response('caselist.html', {
        'viewer': user,
        'cases': case_attributes}, context_instance=RequestContext(request))


@login_required
def display_case(request, case_id, mode='v'):

    ''' Displays the specified case. '''

    user = request.user

    case = Case.objects.filter(id=case_id)[0]

    if request.method == 'POST':

        if mode == 'c':

            priority_form = UpdateCasePriorityForm()
            status_form = UpdateCaseStatusForm()
            adopt_form = UpdateCaseLockHolderForm()
            comment_form = PostCommentForm(request.POST)
            if comment_form.is_valid():

                # Id of the parent, actually
                comment_id = comment_form.cleaned_data['comment_id']

                comments = comment_form.cleaned_data['comments']

                comment = Comment(author=user, text=comments,
                                  time_posted=timezone.now())
                comment.save()

                print "commentID", comment_id
                if comment_id == -1:

                    # Search for a group with the user id.
                    matching_group = None

                    # Check submitter comments for a match
                    if (hasattr(user, "worker") and
                            case.submitter == user.worker):
                        case.submitter_comments.comments.add(comment)
                    else:

                        # Check reviewer comments for a match
                        groups = CommentGroup.objects.all().filter(
                        reviewed_case_set=case)[:]

                        print groups

                        for group in groups:
                            comments = group.comments.all()

                            if len(comments) > 0:
                                author = comments[0].author
                                if author == user:
                                    matching_group = group
                                    break

                        if matching_group == None:
                            matching_group = CommentGroup()
                            matching_group.save()

                        matching_group.comments.add(comment)

                        case.reviewer_comments.add(matching_group)

                else:
                    parent_comment = Comment.objects.filter(id=comment_id)[0]
                    parent_comment.children.add(comment)

                try:
                    case.save()
                except IntegrityError, e:
                    print str(e)
                    print "hard fail"
                    return HttpResponseServerError()

            else:

                print "Invalid PostCommentForm."

            # In any case, clear the comment form.
            comment_form.fields["comments"].initial = ""

        elif mode == 'p':
            priority_form = UpdateCasePriorityForm(request.POST)
            status_form = UpdateCaseStatusForm()
            adopt_form = UpdateCaseLockHolderForm()
            comment_form = PostCommentForm()
            if priority_form.is_valid():

                priority = priority_form.cleaned_data['priority']

                try:
                    case.priority = priority
                    case.save()
                except IntegrityError, e:
                    print str(e)
                    print "hard fail"
                    return HttpResponseServerError()
        
        elif mode == 'a':
            priority_form = UpdateCasePriorityForm()
            status_form = UpdateCaseStatusForm()
            adopt_form = UpdateCaseLockHolderForm(request.POST)
            comment_form = PostCommentForm()
            if adopt_form.is_valid():
                toggle_field = adopt_form.cleaned_data['toggle_field']
                
                if toggle_field == 2:
                    try:
                        print user.doctor.user_first_name()
                        case.lock_holder = user.doctor
                        case.save()
                    except IntegrityError, e:
                        print str(e)
                        print "hard fail"
                        return HttpResponseServerError()
                    
        elif mode == 's':
            priority_form = UpdateCasePriorityForm()
            status_form = UpdateCaseStatusForm(request.POST)
            adopt_form = UpdateCaseLockHolderForm()
            comment_form = PostCommentForm()
            if status_form.is_valid():
                status = status_form.cleaned_data['status']
                try:
                    case.status = status
                    case.save()
                except IntegrityError, e:
                    print str(e)
                    print "hard fail"
                    return HttpResponseServerError()

            else:

                print "Invalid UpdateCasePriorityForm."

        else:

            return HttpResponseServerError("Invalid POST mode.")

    priority_form = UpdateCasePriorityForm()
    priority_form.populate(case)
        
    status_form = UpdateCaseStatusForm()
    status_form.populate(case)
    
    adopt_form = UpdateCaseLockHolderForm()
    adopt_form.populate()

    comment_form = PostCommentForm()

    current_index = BoxedInteger(0)
    submitter_comments = create_comment_group_entries(
        [case.submitter_comments], current_index)[0]
    reviewer_comments = create_comment_group_entries(
        case.reviewer_comments.all(), current_index)

    return render_to_response('case.html', {
        'viewer': user,
        'user': user,
        'case': case,
        'firstName': case.patient.first_name,
        'lastName': case.patient.last_name,
        'patient_id': case.patient.id,
        'gender': case.patient.gender,
        'date_of_birth': case.patient.date_of_birth,
        'health_id': case.patient.health_id,
        'case_id': case_id,
        'priority': case.priority,
        'status': case.status,
        'lock_holder': case.lock_holder,
        'submitter_comments': submitter_comments,
        'reviewer_comments': reviewer_comments,
        'comment_count': current_index.value,
        'priority_form': priority_form,
        'status_form': status_form,
        'comment_form': comment_form,
        'adopt_form': adopt_form,
        'comment_post_action': reverse('display_case', args=[case_id, 'c'])
    }, context_instance=RequestContext(request))
