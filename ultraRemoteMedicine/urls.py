from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ultraRemoteMedicine.views.home', name='home'),
    # url(r'^ultraRemoteMedicine/', include('ultraRemoteMedicine.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('sample.views',
                        url('^$', 'home', name='home'))

urlpatterns += patterns('sample.authentication',
                        url('^login$', 'process_login', name='login'))

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
                        url('^cases$', 'display_case_list', name='case_list'),
                        url('^newcase/(?P<patient_id>\w+)$',
                            'display_new_case', name='new_case'))

urlpatterns += patterns('sample.mobile',
                        url('^mobile/login$', 'process_login'),
                        url('^mobile/add_patient$', 'create_new_patient_m'))

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
                            url(r'^static/(?P<path>.*)$', 'serve'))
