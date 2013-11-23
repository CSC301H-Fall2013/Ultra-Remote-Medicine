from utilities import create_case_attributes
from sample.models import Case
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect


@login_required
def display_field_worker(request):
    ''' Load worker information to worker's display page. '''

    try:
        user = request.user
        worker = request.user.worker
    except ObjectDoesNotExist:
        return HttpResponseRedirect("/")

    case_attributes = create_case_attributes(Case.objects)

    return render_to_response('fieldworker.html', {
        'viewer': user,
        'user': user,
        'phone_number': worker.phone,
        'address': worker.address,
        'registration_time': worker.registration_time,
        'comments': worker.comments,
        'id': worker.id,
        'cases': case_attributes
    }, context_instance=RequestContext(request))
