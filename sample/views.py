import operator

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseBadRequest, HttpResponseRedirect,\
    HttpResponseServerError
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.utils import timezone

from sample.forms import NewPatientForm, NewCaseForm, UpdateFieldWorkerForm,\
    UpdateDoctorForm, UpdateCaseForm
from sample.models import Doctor, Worker, Patient, Case, Comment, CommentGroup


class CaseAttribute():
    ''' A class that contains pre-processed information about a case.
    This is transmitted to the display template. '''

    def __init__(self, case_reference):
        self.case_ref = case_reference
        self.patient_ref = case_reference.patient

        # TODO: Make this value correspond to the actual age.
        self.age = 30


def create_case_attributes(cases):
    ''' Creates a list of CaseAttributes that correspond to the given sub-set
        of cases.'''

    attributes = [CaseAttribute(case) for case in\
                  cases.all()]
    return attributes


class CommentEntry():
    ''' A class that contains a comment that has been cleaned for displaying in
        a view.'''

    def __init__(self, comment_reference):
        ''' Initializes this CommentEntry. Does not recurse through
            children.'''

        self.comment_reference = comment_reference
        self.cleaned_time = comment_reference.time_posted
        self.children = []


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


class CommentGroupEntry():
    ''' A class that contains a comment that has been cleaned for displaying in
        a view.'''

    def __init__(self):
        ''' Initializes this CommentGroupEntry. Does not recurse through
            children.'''

        self.contents = []


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
        print entry.contents
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


def home(request):
    """
    Page to initiate sign-in
    """
    return render_to_response('login.html', {
        # add stuff here
    }, context_instance=RequestContext(request))


def process_login(request):
    """
    Authenticates the user (this assumes https is being used such that the
    password does not need to be encrypted by javascript)
    """

    # Get username and password
    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        return HttpResponseBadRequest()

    # redirections
    signin_page = reverse_lazy("home")  # redirect to login page if failed
    doctor_page = reverse_lazy("doctor")  # redirect to doctor's page
    worker_page = reverse_lazy("field")  # redirect to worker's page

    # Check if username is db
    try:
        User.objects.get(username=username)
    except ObjectDoesNotExist:
        return HttpResponseRedirect("%s?e=u" % signin_page)

    # authenticate the user and then log the user in
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            try:
                Doctor.objects.get(user=user)  # check if doctor
                login(request, user)
                return HttpResponseRedirect(request.POST.get('next',
                                                             doctor_page))
            except ObjectDoesNotExist:  # else the worker
                try:
                    Worker.objects.get(user=user)
                    login(request, user)
                    return HttpResponseRedirect(request.POST.get('next',
                                                                 worker_page))
                except ObjectDoesNotExist:  # if niether worker or doctor
                    # must be admin, but we don't allow admins login from here
                    return HttpResponseRedirect("%s?e=a" % signin_page)
        else:
            # redirect if account is not active
            return HttpResponseRedirect("%s?e=a" % signin_page)
    else:
        # redirect if wrong password
        return HttpResponseRedirect("%s?e=p" % signin_page)


def display_doctor(request):
    ''' Load doctor information to doctor's display page. '''

    user = request.user
    doctor = request.user.doctor

    case_attributes = create_case_attributes(Case.objects)

    return render_to_response('doctor.html', {
        'viewer': user,
        'user': user,
        'phone_number': doctor.phone,
        'address': doctor.address,
        'registration_time': doctor.registration_time,
        'specialties': doctor.specialties.all(),
        'comments': doctor.comments,
        'id': doctor.id,
        'cases': case_attributes
    }, context_instance=RequestContext(request))


def display_field_worker(request):
    ''' Load worker information to worker's display page. '''

    user = request.user
    worker = request.user.worker

    case_attributes = create_case_attributes(Case.objects)

    return render_to_response('fieldworker.html', {
        'viewer': user,
        'user': user,
        'phone_number': worker.phone,
        'address': worker.address,
        'registration_time': worker.registration_time,
        'comments': worker.comments,
        'id': worker.id,
        'cases': case_attributes
    }, context_instance=RequestContext(request))


def display_new_patient(request):
    ''' Display the new patient page and process submitted new-patient
        forms. '''

    if request.method == 'POST':

        form = NewPatientForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            gps_coordinates = form.cleaned_data['gps_coordinates']
            address = form.cleaned_data['address']
            date_of_birth = form.cleaned_data['date_of_birth']
            phone_number = form.cleaned_data['phone_number']
            health_id = form.cleaned_data['health_id']
            photo_link = form.cleaned_data['photo_link']
            sex = form.cleaned_data['sex']
            email = form.cleaned_data['email']

            try:
                patient = Patient(
                    first_name=first_name,
                    last_name=last_name,
                    gps_coordinates=gps_coordinates,
                    address=address,
                    date_of_birth=date_of_birth,
                    phone=phone_number,
                    health_id=health_id,
                    gender=sex,
                    email=email,
                    photo_link=photo_link)
                patient.save()
            except IntegrityError:
                print "hard fail"
                return HttpResponseServerError()

            return HttpResponseRedirect("/patient/" + str(patient.id))
    else:

        # The page has just been entered and so the form hasn't
        # been submitted yet.
        form = NewPatientForm()

    return render_to_response('newPatient.html',
                              {'form': form,
                               'viewer': request.user},
                              context_instance=RequestContext(request))


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


def display_patient(request, patient_id):
    ''' Display patient information. '''

    user = request.user

    patient = Patient.objects.filter(id=patient_id)[0]

    case_attributes = create_case_attributes(Case.objects)

    # Define the filter function for patient cases
    def filter_function(x):
        return x.patient_ref == patient

    case_attributes = filter(filter_function, case_attributes)

    date_of_birth = patient.date_of_birth
    if date_of_birth == None:
        date_of_birth = ""

    return render_to_response('Patient.html', {
        'viewer': user,
        'user': user,
        'photo_link': patient.photo_link,
        'firstName': patient.first_name,
        'lastName': patient.last_name,
        'patient_id': patient.id,
        'gender': patient.gender,
        'date_of_birth': date_of_birth,
        'gps_coordinates': patient.gps_coordinates,
        'health_id': patient.health_id,
        'address': patient.address,
        'phone': patient.phone,
        'email': patient.email,
        'cases': case_attributes,
    }, context_instance=RequestContext(request))


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
        'submitter_comments': create_comment_group_entries(
                [case.submitter_comments])[0],
        'reviewer_comments': create_comment_group_entries(
                case.reviewer_comments.all()),
        'form': form
    }, context_instance=RequestContext(request))


def _display_worker(request, user, worker):
    '''Called by display_profile when it is determined that the user is a
    worker. Displays the profile of the specified worker.

    Precondition: user should correspond to worker. '''

    if request.method == 'POST' and user == request.user:

        form = UpdateFieldWorkerForm(request.POST)
        if form.is_valid():

            try:
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.save()

                worker.phone = form.cleaned_data['phone_number']
                worker.address = form.cleaned_data['address']
                worker.comments = form.cleaned_data['comments']
                worker.save()

            except IntegrityError:
                print "Worker update fail"
                return HttpResponseServerError()
    else:
        form = UpdateFieldWorkerForm()
        form.populate(worker)

    return render_to_response('workerprofile.html', {
        'viewer': request.user,
        'form': form,
        'user': user,
        'phone_number': worker.phone,
        'address': worker.address,
        'registration_time': worker.registration_time,
        'comments': worker.comments,
        'id': worker.id
    }, context_instance=RequestContext(request))


def _display_doctor(request, user, doctor):
    '''Called by display_profile when it is determined that the user is a
    doctor. Displays the profile of the specified doctor.

    Precondition: user should correspond to doctor. '''

    if request.method == 'POST' and user == request.user:

        form = UpdateDoctorForm(request.POST)
        if form.is_valid():

            try:
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.save()

                doctor.phone = form.cleaned_data['phone_number']
                doctor.address = form.cleaned_data['address']
                doctor.comments = form.cleaned_data['comments']
                doctor.save()

            except IntegrityError:
                print "Doctor update fail"
                return HttpResponseServerError()
    else:
        form = UpdateDoctorForm()
        form.populate(doctor)

    return render_to_response('doctorprofile.html', {
        'viewer': request.user,
        'form': form,
        'user': user,
        'phone_number': doctor.phone,
        'address': doctor.address,
        'registration_time': doctor.registration_time,
        'specialties': doctor.specialties.all(),
        'comments': doctor.comments,
        'id': doctor.id
    }, context_instance=RequestContext(request))


def display_profile(request, user_id):
    '''Displays the profile page of a user. Does not allow editing (protected
        at both view and model levels) of another user's profile.'''

    user = User.objects.filter(id=user_id)[0]

    if hasattr(user, "worker"):
        return _display_worker(request, user, user.worker)
    else:
        return _display_doctor(request, user, user.doctor)


def change_doctor_info(request):
    ''' Andrew: Despite the fact that we don't use this, I'm leaving it in
        because the server won't run if I get rid of it.'''

    doctor = request.user.doctor
#     try:
#         doctor.first_name=first_name,
#         doctor.last_name=last_name,
#         doctor.phone=phone_number,
#         doctor.address=address,
#         doctor.specialties=specialties
#         doctor.schedule=schedule
#         doctor.cases=cases
#         doctor.save()
#     except IntegrityError:
#         print "hard fail"
#         return HttpResponseServerError()

    case_attributes = create_case_attributes(Case.objects)

    return render_to_response('doctor.html', {
        'name': doctor.user.first_name,
        'last_name': doctor.user.last_name,
        'phone': doctor.phone,
        'address': doctor.address,
        'specialties': doctor.specialties.all(),
        'schedule': doctor.schedule.all(),
        'cases': case_attributes
    }, context_instance=RequestContext(request))


def change_worker_info(request):

    worker = request.user.worker
#     try:
#         worker.first_name=first_name,
#         worker.last_name=last_name,
#         worker.phone=phone_number,
#         worker.address=address,
#         worker.specialties=specialties
#         worker.schedule=schedule
#         worker.cases=cases
#         worker.save()
#     except IntegrityError:
#         print "hard fail"
#         return HttpResponseServerError()

    case_attributes = create_case_attributes(Case.objects)

    return render_to_response('fieldworker.html', {
        'name': worker.user.first_name,
        'last_name': worker.user.last_name,
        'phone': worker.phone,
        'address': worker.address,
        'id': worker.id,
        'cases': case_attributes
    }, context_instance=RequestContext(request))
