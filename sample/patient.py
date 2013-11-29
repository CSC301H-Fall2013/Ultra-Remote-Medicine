from sample.forms import NewPatientForm
from sample.models import Patient
from django.db import IntegrityError
from django.http import HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from utilities import create_case_attributes
from sample.models import Case
from django.contrib.auth.decorators import login_required



@login_required
def display_new_patient(request):
    ''' Display the new patient page and process submitted new-patient
        forms. '''

    if request.method == 'POST':

        form = NewPatientForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            gps_coordinates = form.cleaned_data['gps_coordinates']
            address = form.cleaned_data['address']
            date_of_birth = form.cleaned_data['date_of_birth']
            phone_number = form.cleaned_data['phone_number']
            health_id = form.cleaned_data['health_id']
            sex = form.cleaned_data['sex']
            email = form.cleaned_data['email']
            patient_pic = form.cleaned_data['patient_pic']

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
                    patient_pic=patient_pic)
                patient.save()
            except IntegrityError:
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


@login_required
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
    if date_of_birth is None:
        date_of_birth = ""

    return render_to_response('patient.html', {
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
        'patient_pic': patient.patient_pic
    }, context_instance=RequestContext(request))
