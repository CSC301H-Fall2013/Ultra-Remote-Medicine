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
from sample.models import Case, Comment, CommentGroup, Scan
from django.utils import timezone
from base64 import b64decode
from django.core.files.base import ContentFile


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
                json_data['worker'] = user.worker
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
                                    "type": "newPatient", "patient_id":
                                    str(patient.id)})
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

    try:
        patient = Patient.objects.filter(id=data['patient_id'])[0]
    except KeyError:
        json_response = json.dumps({"success": "false",
                                    "type": "KeyError"})
        return HttpResponse(json_response, mimetype='application/json')

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

    form = NewCaseForm(data)
    worker = data['worker']

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
                                    "type": "newCase",
                                    "case_id": str(case.id)})
        return HttpResponse(json_response, mimetype='application/json')
    else:
        json_response = json.dumps({"success": "false",
                                    "type": "invalidForm"})
        return HttpResponse(json_response, mimetype='application/json')


@csrf_exempt
def display_case_m(request):

    ''' Displays the specified case. '''

    data = is_worker(request)
    if not data:
        json_response = json.dumps({"success": "false",
                                    "type": "notWorker"})
        return HttpResponse(json_response, mimetype='application/json')

    try:
        case = Case.objects.filter(id=data['case_id'])[0]
    except KeyError:
        json_response = json.dumps({"success": "false",
                                    "type": "KeyError"})
        return HttpResponse(json_response, mimetype='application/json')

    json_response = json.dumps({"success": "true",
                                "type": "newCase",
                                'firstName': str(case.patient.first_name),
                                'lastName': str(case.patient.last_name),
                                'patient_id': str(case.patient.id),
                                'gender': str(case.patient.gender),
                                'date_of_birth':
                                str(case.patient.date_of_birth),
                                'health_id': str(case.patient.health_id),
                                'priority': str(case.priority)})
    return HttpResponse(json_response, mimetype='application/json')


@csrf_exempt
def upload_image_m(request):

    data = is_worker(request)
    if not data:
        json_response = json.dumps({"success": "false",
                                    "type": "notWorker"})
        return HttpResponse(json_response, mimetype='application/json')

    try:
        case = Case.objects.filter(id=data['case_id'])[0]
    except KeyError:
        json_response = json.dumps({"success": "false",
                                    "type": "KeyError"})
        return HttpResponse(json_response, mimetype='application/json')

    try:
        scan = Scan(
            patient=case.patient)
        scan.save()
    except IntegrityError:
        scan.delete()
        json_response = json.dumps({"success": "false",
                                    "type": "IntegrityError"})
        return HttpResponse(json_response, mimetype='application/json')

    try:
        image_data = b64decode(data['image_string'])
        scan.file = ContentFile(image_data)
        scan.save()
        case.scan = scan
        case.save()
    except IntegrityError:
        json_response = json.dumps({"success": "false",
                                    "type": "IntegrityError"})
        return HttpResponse(json_response, mimetype='application/json')

    json_response = json.dumps({"success": "true",
                                "type": "uploadSuccess"})
    return HttpResponse(json_response, mimetype='application/json')


@csrf_exempt
def display_patient_cases_m(request):

    ''' Displays all cases related to a patient. '''

    data = is_worker(request)
    if not data:
        json_response = json.dumps({"success": "false",
                                    "type": "notWorker"})
        return HttpResponse(json_response, mimetype='application/json')

    try:
        patient = Patient.objects.filter(id=data['patient_id'])[0]
        cases = Case.objects.filter(patient=patient)
    except KeyError:
        json_response = json.dumps({"success": "false",
                                    "type": "KeyError"})
        return HttpResponse(json_response, mimetype='application/json')

    json_response = json.dumps({"success": "true",
                                "type": "patientCases",
                                "cases": create_cases_json(cases)})
    return HttpResponse(json_response, mimetype='application/json')


def create_cases_json(case_objects):

    case = {}
    cases = []
    for case_object in case_objects:
        case['firstName'] = str(case_object.patient.first_name)
        case['lastName'] = str(case_object.patient.last_name)
        case['patient_id'] = str(case_object.patient.id)
        case['gender'] = str(case_object.patient.gender)
        case['date_of_birth'] = str(case_object.patient.date_of_birth)
        case['health_id'] = str(case_object.patient.health_id)
        case['priority'] = str(case_object.priority)
        cases.append(case)
        case = {}

    return cases
