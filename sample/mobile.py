import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.db import IntegrityError
from sample.forms import NewPatientForm
from sample.models import Patient
from django.utils.importlib import import_module
from django.contrib.auth import get_user
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, load_backend
from sample.models import Case
from utilities import create_case_attributes


def is_worker(session_key):

    engine = import_module(settings.SESSION_ENGINE)
    session = engine.SessionStore(session_key)

    try:
        worker = session[SESSION_KEY]
        sample_path = session[BACKEND_SESSION_KEY]
        sample = load_backend(sample_path)
        user = sample.get_user(worker) or AnonymousUser()
    except KeyError:
        user = AnonymousUser()

    if user.is_authenticated():
        try:
            return user.worker
        except:
            return False


@csrf_exempt
def process_login(request):

    json_data = json.loads(request.raw_post_data)
    try:
        username = json_data['username']
        password = json_data['password']
    except KeyError:
        json_response = json.dumps({"success": "false",
                                    "type": "badRequest"})
        return HttpResponse(json_response, mimetype='application/json')

    try:
        User.objects.get(username=username)
    except ObjectDoesNotExist:
        json_response = json.dumps({"success": "false",
                                    "type": "invalidUser"})
        return HttpResponse(json_response, mimetype='application/json')

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            try:
                login(request, user)
                json_response = json.dumps({"success": "true",
                                            "type": "worker",
                                            "sessionid":
                                            request.session.session_key})
                return HttpResponse(json_response, mimetype='application/json')
            except ObjectDoesNotExist:
                json_response = json.dumps({"success": "false",
                                            "type": "existence"})
                return HttpResponse(json_response, mimetype='application/json')
        else:
            json_response = json.dumps({"success": "false", "type": "active"})
            return HttpResponse(json_response, mimetype='application/json')
    else:
        # bad password
        json_response = json.dumps({"success": "false", "type": "password"})
        return HttpResponse(json_response, mimetype='application/json')


@csrf_exempt
def create_new_patient_m(request):

    json_data = json.loads(request.raw_post_data)

    try:
        worker = is_worker(json_data['session_key'])
        if not worker:
            json_response = json.dumps({"success": "false",
                                        "type": "notWorker"})
            return HttpResponse(json_response, mimetype='application/json')
    except:
        json_response = json.dumps({"success": "false",
                                    "type": "badRequest"})
        return HttpResponse(json_response, mimetype='application/json')

    form = NewPatientForm(json_data)
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
            json_response = json.dumps({"success": "false",
                                        "type": "IntegrityError"})
            return HttpResponse(json_response, mimetype='application/json')

        json_response = json.dumps({"success": "true",
                                    "type": "newPatient"})
        return HttpResponse(json_response, mimetype='application/json')


@csrf_exempt
def display_patient_m(request):

    json_data = json.loads(request.raw_post_data)

    try:
        worker = is_worker(json_data['session_key'])
        if not worker:
            json_response = json.dumps({"success": "false",
                                        "type": "notWorker"})
            return HttpResponse(json_response, mimetype='application/json')
    except:
        json_response = json.dumps({"success": "false",
                                    "type": "badRequest"})
        return HttpResponse(json_response, mimetype='application/json')

    patient = Patient.objects.filter(id=json_data['patient_id'])[0]

    case_attributes = create_case_attributes(Case.objects)

    # Define the filter function for patient cases
    def filter_function(x):
        return x.patient_ref == patient

    case_attributes = filter(filter_function, case_attributes)

    date_of_birth = patient.date_of_birth
    if date_of_birth is None:
        date_of_birth = ""

    json_response = json.dumps({
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
        'cases': case_attributes})

    return HttpResponse(json_response, mimetype='application/json')
