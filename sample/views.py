from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseBadRequest, HttpResponseRedirect,\
    HttpResponse
from sample.models import Doctor, Worker
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
import pdb

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
    #pdb.set_trace()

    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        return HttpResponseBadRequest()

    signin_page = reverse_lazy("home")
    doctor_page = reverse_lazy("doctor")
    worker_page = reverse_lazy("worker")

    try:
        User.objects.get(username=username)
    except ObjectDoesNotExist:
        return HttpResponseRedirect("%s?e=u" % signin_page)

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            try:
                Doctor.objects.get(user=user)
                login(request, user)
                #return HttpResponseRedirect(request.POST.get('next',
                 #                                            doctor_page))
                return HttpResponse("OK")
            except ObjectDoesNotExist:
                try:
                    Worker.objects.get(user=user)
                    login(request, user)
                    #return HttpResponseRedirect(request.POST.get('next',
                    #                                             worker_page))
                    return HttpResponse("OK")
                except ObjectDoesNotExist:
                    return HttpResponse("Admin does not allow to login here")
        else:
            # inactive account
            return HttpResponseRedirect("%s?e=a" % signin_page)
    else:
        # bad password
        return HttpResponseRedirect("%s?e=p" % signin_page)
