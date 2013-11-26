from django.shortcuts import render_to_response
from django.template import RequestContext


def home(request, status='g'):
    """
    Page to initiate sign-in
    """

    print "The status was: ", status
    
    return render_to_response('login.html', {
        'status': status        
    }, context_instance=RequestContext(request))
