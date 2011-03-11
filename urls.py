from django.conf.urls.defaults import *
from django.contrib import admin
import settings

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    (r'^login/$', 'django.contrib.auth.views.login',  {
        'template_name': 'login.html'}),

    (r'^media/(.*)$', 'django.views.static.serve',
        {'document_root': settings.DEPLOY_PATH + '/media'}),
    (r'^(favicon.ico)$', 'django.views.static.serve',
        {'document_root': settings.DEPLOY_PATH + '/media'}),
    (r'^', include('conlot.main.urls')),
)
