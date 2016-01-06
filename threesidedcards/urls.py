from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'threesidedcards.views.home'),
    url(r'^getItems/$', 'threesidedcards.views.getItems'),
    url(r'^getTriples/$', 'threesidedcards.views.getTriples'),
    url(r'^submit/$', 'threesidedcards.views.submit'),
    url(r'^login/$', 'threesidedcards.views.login'),
    url(r'^logout/$', 'threesidedcards.views.logout'),
    url(r'^addr/$', 'threesidedcards.views.addr'),
    url(r'^status/$', 'threesidedcards.views.status'),
    url(r'^statusData/$', 'threesidedcards.views.statusData'),
)
