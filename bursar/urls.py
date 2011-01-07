from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('bursar.views',
    (r'^$', 'home'),
    (r'^transaction/add','add'),
    (r'^transactions/update','update')
)
