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
    url('^$', 'home', name='home'),
    url('^login$', 'process_login', name='login'),
    url('^doctor$', 'display_doctor', name='doctor'),
    url('^field$', 'display_field_worker', name='field'),
    url('^new_patient$', 'display_new_patient', name='new_patient'),
    url('^view_patient/(?P<patient_id>\d+)$',
        'display_patient', name='display_patient'),
    url('display_case/(?P<case_id>\d+)$',
        'display_case', name='display_case'))


if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
                            url(r'^static/(?P<path>.*)$', 'serve'))
