from django.conf.urls import patterns, include, url
import threesidedcards.views

from flashcards.settings import BASE_URL

urlpatterns = [
    url(r'^' + BASE_URL+ '$', threesidedcards.views.home),
    url(r'^' + BASE_URL+ 'getItems/$', threesidedcards.views.getItems),
    url(r'^' + BASE_URL+ 'getTriples/$', threesidedcards.views.getTriples),
    url(r'^' + BASE_URL+ 'submit/$', threesidedcards.views.submit),
    url(r'^' + BASE_URL+ 'login/$', threesidedcards.views.login),
    url(r'^' + BASE_URL+ 'logout/$', threesidedcards.views.logout),
    url(r'^' + BASE_URL+ 'addr/$', threesidedcards.views.addr),
    url(r'^' + BASE_URL+ 'status/$', threesidedcards.views.status),
    url(r'^' + BASE_URL+ 'statusData/', threesidedcards.views.statusData),
]
