import os
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)))

urlpatterns += patterns('',
                        (r'^media/(.*)$',
                         'django.views.static.serve',
                         {'document_root': settings.MEDIA_ROOT}))

urlpatterns += patterns('sample.views',
                        url('^$', 'home', name='home'),
                        url('^login/(?P<status>\w+)$', 'home', name='home'))

urlpatterns += patterns('sample.authentication',
                        url('^login$', 'process_login', name='login'),
                        url('^logout$', 'process_logout', name='logout'))

urlpatterns += patterns('sample.doctor',
                        url('^doctor$', 'display_doctor', name='doctor'))

urlpatterns += patterns('sample.worker',
                        url('^field$', 'display_field_worker', name='field'))

urlpatterns += patterns('sample.patient',
                        url('^new_patient$', 'display_new_patient',
                            name='new_patient'),
                        url('^patient/(?P<patient_id>\d+)$',
                            'display_patient', name='display_patient'))

urlpatterns += patterns('sample.profiles',
                        url('^profile/(?P<user_id>\d+)$',
                            'display_profile', name='display_profile'))


urlpatterns += patterns('sample.case',
                        url('^case/(?P<case_id>\d+)$', 'display_case',
                            name='display_case'),
                        url('^case/(?P<case_id>\d+)/(?P<mode>\w+)$',
                            'display_case', name='display_case'),
                        url('^cases$', 'display_case_list', name='case_list'),
                        url('^newcase/(?P<patient_id>\w+)$',
                            'display_new_case', name='new_case'))

urlpatterns += patterns('sample.mobile',
                        url('^mobile/login$', 'process_login'),
                        url('^mobile/add_patient$', 'create_new_patient_m'),
                        url('^mobile/view_patient$', 'display_patient_m'),
                        url('^mobile/add_case$', 'create_new_case_m'),
                        url('^mobile/view_case$', 'display_case_m'),
                        url('^mobile/upload$', 'upload_image_m'),
                        url('^mobile/display_patient_cases$',
                            'display_patient_cases_m'),
                        url('^mobile/search$', 'search_patients'))

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
                            url(r'^static/(?P<path>.*)$', 'serve'))
