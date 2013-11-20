from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from sample.models import Worker
import simplejson as sj

def mobile_login(request):
    if request.GET.get('format', '') == 'json':
        try:
            username = request.GET['username']
            password = request.GET['password']
        except KeyError:
            json = {}
            json['status'] = 'no'
            return HttpResponse(sj.dumps(json))

        # Check if username is db
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            json = {}
            json['status'] = 'no'
            return HttpResponse(sj.dumps(json))
        # authenticate the user and then log the user in
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                try:
                    Worker.objects.get(user=user)
                    login(request, user)
                    data = {}
                    data['name'] = username
                    data['password'] = password
                    response = {}
                    response['data'] = data
                    json = {}
                    json['response'] = response
                    json['status'] = 'ok'
                    return HttpResponse(sj.dumps(json))
                except ObjectDoesNotExist:  # if not worker
                    json = {}
                    json['status'] = 'no'
                    return HttpResponse(sj.dumps(json))
            else:
                # redirect if account is not active
                json = {}
                json['status'] = 'no'
                return HttpResponse(sj.dumps(json))
        else:
            # redirect if wrong password
            json = {}
            json['status'] = 'no'
            return HttpResponse(sj.dumps(json))
