from django.shortcuts import render_to_response
from django.template import RequestContext


def home(request):
    """
    Page to initiate sign-in
    """
    return render_to_response('login.html', {
        # add stuff here
    }, context_instance=RequestContext(request))


# def change_doctor_info(request):
#     ''' Andrew: Despite the fact that we don't use this, I'm leaving it in
#         because the server won't run if I get rid of it.'''

#     doctor = request.user.doctor
# #     try:
# #         doctor.first_name=first_name,
# #         doctor.last_name=last_name,
# #         doctor.phone=phone_number,
# #         doctor.address=address,
# #         doctor.specialties=specialties
# #         doctor.schedule=schedule
# #         doctor.cases=cases
# #         doctor.save()
# #     except IntegrityError:
# #         print "hard fail"
# #         return HttpResponseServerError()

#     case_attributes = create_case_attributes(Case.objects)

#     return render_to_response('doctor.html', {
#         'name': doctor.user.first_name,
#         'last_name': doctor.user.last_name,
#         'phone': doctor.phone,
#         'address': doctor.address,
#         'specialties': doctor.specialties.all(),
#         'schedule': doctor.schedule.all(),
#         'cases': case_attributes
#     }, context_instance=RequestContext(request))


# def change_worker_info(request):

#     worker = request.user.worker
# #     try:
# #         worker.first_name=first_name,
# #         worker.last_name=last_name,
# #         worker.phone=phone_number,
# #         worker.address=address,
# #         worker.specialties=specialties
# #         worker.schedule=schedule
# #         worker.cases=cases
# #         worker.save()
# #     except IntegrityError:
# #         print "hard fail"
# #         return HttpResponseServerError()

#     case_attributes = create_case_attributes(Case.objects)

#     return render_to_response('fieldworker.html', {
#         'name': worker.user.first_name,
#         'last_name': worker.user.last_name,
#         'phone': worker.phone,
#         'address': worker.address,
#         'id': worker.id,
#         'cases': case_attributes
#     }, context_instance=RequestContext(request))
