from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseBadRequest, HttpResponseRedirect,\
    HttpResponseServerError
from sample.models import Doctor, Worker, Patient, Case
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from django.db import IntegrityError

class CaseAttribute():
    '''
    A class that contains pre-processed information about a case.
    This is transmitted to the display template.
    '''
    
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
    
    doctor = request.user.doctor

    case_attributes = create_case_attributes(Case.objects)

    return render_to_response('doctor.html', {
        'name': doctor.user.first_name,
        'last_name': doctor.user.last_name,
        'phone': doctor.phone,
        'address': doctor.address,
        'specialties' : doctor.specialties.all(),
        'schedule' : doctor.schedule.all(),
        'cases' : case_attributes
    }, context_instance=RequestContext(request))


def display_field_worker(request):
    ''' Load worker information to worker's display page. '''
    
    worker = request.user.worker

    case_attributes = create_case_attributes(Case.objects)

    return render_to_response('fieldworker.html', {
        'name': worker.user.first_name,
        'last_name': worker.user.last_name,
        'phone': worker.phone,
        'address': worker.address,
        'id': worker.id,
        'cases' : case_attributes
    }, context_instance=RequestContext(request))


def redirect_patient(request):
    ''' Redirect to new patient page. '''
    return render_to_response('newPatient.html', {},
                              context_instance=RequestContext(request))

def add_patient(request):
    ''' Add new patient by retrieving information and creating a new object
    in database. '''

    try:
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        patient_ID = request.POST['patientID']
        phone_number = request.POST['phoneNumber']
        gps_coordinates = request.POST['gpsCoordinates']
        address = request.POST['address']
        comment = request.POST['comments']
    except KeyError:
        print "Fail"
        return HttpResponseBadRequest()

    try:
        patient = Patient(
            first_name=first_name,
            last_name=last_name,
            phone=phone_number,
            gps_coordinates=gps_coordinates,
            address=address,
            health_id=patient_ID)
        patient.save()
    except IntegrityError:
        print "hard fail"
        return HttpResponseServerError()

    # TODO: Filter these so that they are only cases regarding the patient.
    case_attributes = create_case_attributes(Case.objects)
    
    return render_to_response('patient.html', {
        'firstName': patient.first_name,
        'lastName': patient.last_name,
        'phone': patient.phone,
        'address': patient.address,
        'cases' : case_attributes
    }, context_instance=RequestContext(request))
