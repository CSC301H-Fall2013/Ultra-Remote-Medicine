import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist


@csrf_exempt
def process_login(request):
    incomingData = json.loads(request.raw_post_data)

    try:
        username = incomingData['username']
        password = incomingData['password']
    except KeyError:
        return HttpResponseBadRequest()

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            try:
                login(request, user)
                json_response = json.dumps({"success": "true", "type": "doctor",
                                            "sessionid":
                                            request.session.session_key})
                return HttpResponse(json_response, mimetype='application/json')
            except ObjectDoesNotExist:
                login(request, user)
                json_response = json.dumps({"success": "true", "type": "worker"})
                return HttpResponse(json_response, mimetype='application/json')
        else:
            json_response = json.dumps({"success": "false", "type": "active"})
            return HttpResponse(json_response, mimetype='application/json')
    else:
        # bad password
        json_response = json.dumps({"success": "false", "type": "password"})
        return HttpResponse(json_response, mimetype='application/json')
