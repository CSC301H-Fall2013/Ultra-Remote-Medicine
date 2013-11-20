from django.contrib.auth.models import User
from sample.models import TimeSlot
from sample.forms import UpdateFieldWorkerForm, UpdateDoctorForm
from django.db import IntegrityError
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseServerError


class TimeSlotDisplay:
    
    def __init__(self, original, is_last):
        if is_last:
            self.time_string = original.to_string()
        else:
            self.time_string = original.to_string() + ","

def display_profile(request, user_id):
    '''Displays the profile page of a user. Does not allow editing (protected
        at both view and model levels) of another user's profile.'''

    user = User.objects.filter(id=user_id)[0]

    if hasattr(user, "worker"):
        return _display_worker(request, user, user.worker)
    else:
        return _display_doctor(request, user, user.doctor)


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

    # Create Timeslot client-side objects
    time_slots = []
    is_last = False
    i=1
    for original in doctor.schedule.all():
        if len(doctor.schedule.all()) == i:
            is_last = True
        time_slots.append(TimeSlotDisplay(original, is_last))
        i+=1

    return render_to_response('doctorprofile.html', {
        'viewer': request.user,
        'form': form,
        'user': user,
        'phone_number': doctor.phone,
        'address': doctor.address,
        'registration_time': doctor.registration_time,
        'specialties': doctor.specialties.all(),
        'schedule': time_slots,
        'comments': doctor.comments,
        'id': doctor.id
    }, context_instance=RequestContext(request))
