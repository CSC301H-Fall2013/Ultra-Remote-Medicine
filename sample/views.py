from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseBadRequest, HttpResponseRedirect,\
    HttpResponseServerError
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from django.db import IntegrityError

from sample.forms import NewPatientForm, UpdateFieldWorkerForm,\
    UpdateDoctorForm
from sample.models import Doctor, Worker, Patient, Case


class CaseAttribute():
    ''' A class that contains pre-processed information about a case.
    This is transmitted to the display template. '''

    def __init__(self, case_reference):
        self.case_ref = case_reference
        self.patient_ref = case_reference.patient
        self.age = 30


def create_case_attributes(cases):
    ''' Creates a list of CaseAttributes that correspond to all known cases.'''

    attributes = [CaseAttribute(case) for case in\
                  cases.all()]
    return attributes


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
            # photo_link = form.cleaned_data['photo_link']
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
                    email=email)
                patient.save()
            except IntegrityError:
                print "hard fail"
                return HttpResponseServerError()

            return HttpResponseRedirect("patient/" +
                str(patient.id))
    else:

        # The page has just been entered and so the form hasn't
        # been submitted yet.
        form = NewPatientForm()

    return render_to_response('newPatient.html', 
                              {'form': form,
                               'viewer': request.user},
                              context_instance=RequestContext(request))


def display_patient(request, patient_id):
    ''' Display patient information. '''

    user = request.user

    # TODO: Filter these so that they are only cases regarding the patient.
    case_attributes = create_case_attributes(Case.objects)

    patient = Patient.objects.filter(id=patient_id)[0]

    return render_to_response('Patient.html', {
        'viewer': user,
        'user': user,
        'firstName': patient.first_name,
        'lastName': patient.last_name,
        'phone': patient.phone,
        'address': patient.address,
        'cases': case_attributes
    }, context_instance=RequestContext(request))


def display_case(request, case_id):
    ''' Displays the specified case. '''

    user = request.user

    case = Case.objects.filter(id=case_id)[0]

    return render_to_response('Case.html', {
        'user': user
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
