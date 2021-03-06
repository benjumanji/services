from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'services.views.home'),
    (r'^bursar/',include('services.bursar.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^assets/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT})
)
