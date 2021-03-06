from utilities import create_case_attributes
from sample.models import Case
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist


@login_required
def display_doctor(request):
    ''' Load doctor information to doctor's display page. '''

    try:
        user = request.user
        doctor = request.user.doctor
    except ObjectDoesNotExist:
        return HttpResponseRedirect("/")

    case_attributes = create_case_attributes(Case.objects)

    return render_to_response('doctor.html', {
        'viewer': user,
        'user': user,
        'phone_number': doctor.phone,
        'address': doctor.address,
        'registration_time': doctor.registration_time,
        'specialties': doctor.specialties.all(),
        'schedule': 'hohoho',
        'comments': doctor.comments,
        'id': doctor.id,
        'cases': case_attributes
    }, context_instance=RequestContext(request))
