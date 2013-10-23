from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from sample.models import Doctor, Worker
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login


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
    '''Load doctor information to doctor's display page'''
    doctor = request.user.doctor

    return render_to_response('doctor.html', {
        'name': doctor.user.first_name,
        'last_name': doctor.user.last_name,
        'phone': doctor.phone,
        'address': doctor.address,
    }, context_instance=RequestContext(request))


def display_field_worker(request):
    '''Load worker information to worker's display page'''
    worker = request.user.worker

    return render_to_response('fieldworker.html', {
        'name': worker.user.first_name,
        'last_name': worker.user.first_name,
        'phone': worker.phone,
        'address': worker.address,
        'id': worker.id
    }, context_instance=RequestContext(request))
