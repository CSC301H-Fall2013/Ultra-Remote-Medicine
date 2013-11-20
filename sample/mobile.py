import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.db import IntegrityError
from sample.forms import NewPatientForm, NewCaseForm
from sample.models import Patient
from django.utils.importlib import import_module
from django.contrib.auth import get_user
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, load_backend
from sample.models import Case, Comment, CommentGroup
from utilities import create_case_attributes
from django.utils import timezone


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


def is_worker(request):

    json_data = json.loads(request.raw_post_data)

    engine = import_module(settings.SESSION_ENGINE)
    try:
        session = engine.SessionStore(json_data['session_key'])
    except KeyError:
        json_response = json.dumps({"success": "false",
                                    "type": "badRequest"})
        return HttpResponse(json_response, mimetype='application/json')

    try:
        worker = session[SESSION_KEY]
        sample_path = session[BACKEND_SESSION_KEY]
        sample = load_backend(sample_path)
        user = sample.get_user(worker) or AnonymousUser()
    except KeyError:
        user = AnonymousUser()

    if user.is_authenticated():
        try:
            if user.worker:
                return json_data
        except:
            return False


@csrf_exempt
def create_new_patient_m(request):

    data = is_worker(request)
    if not data:
        json_response = json.dumps({"success": "false",
                                    "type": "notWorker"})
        return HttpResponse(json_response, mimetype='application/json')

    form = NewPatientForm(data)
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
    else:
        json_response = json.dumps({"success": "false",
                                    "type": "invalidForm"})
        return HttpResponse(json_response, mimetype='application/json')


@csrf_exempt
def display_patient_m(request):

    data = is_worker(request)
    if not data:
        json_response = json.dumps({"success": "false",
                                    "type": "notWorker"})
        return HttpResponse(json_response, mimetype='application/json')

    patient = Patient.objects.filter(id=data['patient_id'])[0]

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
        'date_of_birth': date_of_birth.strftime('%Y-%m-%d'),
        'gps_coordinates': patient.gps_coordinates,
        'health_id': patient.health_id,
        'address': patient.address,
        'phone': patient.phone,
        'email': patient.email})

    return HttpResponse(json_response, mimetype='application/json')

@csrf_exempt
def create_new_case_m(request):

    data = is_worker(request)
    if not data:
        json_response = json.dumps({"success": "false",
                                    "type": "notWorker"})
        return HttpResponse(json_response, mimetype='application/json')

    form = NewCaseForm(is_worker(data))
    worker = request.user.worker
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
        except IntegrityError:
            json_response = json.dumps({"success": "false",
                                        "type": "IntegrityError"})
            return HttpResponse(json_response, mimetype='application/json')

        json_response = json.dumps({"success": "true",
                                    "type": "newCase"})
        return HttpResponse(json_response, mimetype='application/json')
    else:
        json_response = json.dumps({"success": "false",
                                    "type": "invalidForm"})
        return HttpResponse(json_response, mimetype='application/json')
