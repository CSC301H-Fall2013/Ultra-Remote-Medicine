from django.shortcuts import render_to_response
from django.template import RequestContext


def home(request):
    """
    Page to initiate sign-in
    """
    return render_to_response('login.html', {
        # add stuff here
    }, context_instance=RequestContext(request))
