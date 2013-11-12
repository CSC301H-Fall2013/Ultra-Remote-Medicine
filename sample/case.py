from sample.forms import NewCaseForm, UpdateCaseForm
from sample.models import Patient, Comment, Case, CommentGroup
from django.utils import timezone
from django.db import IntegrityError
from django.shortcuts import render_to_response
from django.template import RequestContext
from utilities import create_case_attributes
from django.http import HttpResponseRedirect, HttpResponseServerError


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
                    author=worker.user,
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


def display_case_list(request):
    ''' Displays the list of cases.'''

    user = request.user

    case_attributes = create_case_attributes(Case.objects)

    return render_to_response('caselist.html', {
        'viewer': user,
        'cases': case_attributes}, context_instance=RequestContext(request))


def display_case(request, case_id):
    ''' Displays the specified case. '''

    user = request.user

    case = Case.objects.filter(id=case_id)[0]

    if request.method == 'POST':

        form = UpdateCaseForm(request.POST)
        if form.is_valid():

            priority = form.cleaned_data['priority']

            try:
                case.priority = priority
                case.save()
            except IntegrityError, e:
                print str(e)
                print "hard fail"
                return HttpResponseServerError()

    else:

        # The page has just been entered and so the form hasn't
        # been submitted yet.
        form = UpdateCaseForm()
        form.populate(case)

    return render_to_response('case.html', {
        'viewer': user,
        'user': user,
        'firstName': case.patient.first_name,
        'lastName': case.patient.last_name,
        'patient_id': case.patient.id,
        'gender': case.patient.gender,
        'date_of_birth': case.patient.date_of_birth,
        'health_id': case.patient.health_id,
        'case_id': case_id,
        'submitter_comments':
        create_comment_group_entries([case.submitter_comments])[0],
        'reviewer_comments':
        create_comment_group_entries(case.reviewer_comments.all()),
        'form': form
    }, context_instance=RequestContext(request))


class CommentEntry():
    ''' A class that contains a comment that has been cleaned for displaying in
        a view.'''

    def __init__(self, comment_reference):
        ''' Initializes this CommentEntry. Does not recurse through
            children.'''

        self.comment_reference = comment_reference
        self.cleaned_time = comment_reference.time_posted
        self.children = []


class CommentGroupEntry():
    ''' A class that contains a comment that has been cleaned for displaying in
        a view.'''

    def __init__(self):
        ''' Initializes this CommentGroupEntry. Does not recurse through
            children.'''

        self.contents = []


def create_comment_entries(comments):
    ''' Creates view-ready comment entries that correspond to the given list
        of comments. This will recurse through children as well. At all levels,
        the comments are sorted by time posted.
        '''

    sorted_comments = comments.order_by('-time_posted')

    entries = []
    for comment in sorted_comments:
        entry = CommentEntry(comment)
        entry.children = create_comment_entries(comment.children)
        entries.append(entry)

    return entries


def create_comment_group_entries(comment_groups):
    ''' Creates view-ready comment group entries that correspond to the given
        list of comment groups. This will recurse through the comments and
        their children as well. At all levels, the comments are sorted by time
        posted. The groups are sorted by the latest time posted.

        comments may be of type django.db.models.manager.Manager or Comment.'''

    entries = []
    for comment_group in comment_groups:
        entry = CommentGroupEntry()
        entry.contents = create_comment_entries(comment_group.comments)
        entries.append(entry)

    # The function to use in order to sort groups according to which has last
    # been updated.
    def compare_group(x, y):
        x_older = (x.contents[0].comment_reference.time_posted <
                   y.contents[0].comment_reference.time_posted)

        if x_older:
            return 1
        else:
            return -1

    entries.sort(cmp=compare_group)
    return entries
