from django.conf.urls.defaults import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'webapp.views.home'),
#    url(r'^graph/$', 'webapp.views.graph'), 
    url(r'^idea/(?P<id>\d+)/$', 'webapp.views.idea'),
    url(r'^ajax/upvote/$', 'webapp.views.upvote'),
    url(r'^ajax/addidea/$', 'webapp.views.addidea'),
    url(r'^ajax/addsuggestion/$', 'webapp.views.addsuggestion'),
    url(r'^ajax/autocomplete/$', 'webapp.views.autocomplete'),    
    url(r'^ajax/getIdeaById/$', 'webapp.views.getIdeaById'),    
    url(r'^admin/', include(admin.site.urls)),
)
