from django.shortcuts import render
from threesidedcards.models import *
from threesidedcards.defaultpassword import *

from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.core.urlresolvers import reverse


from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from django.db import IntegrityError, transaction

import random


def addr(request):
    return HttpResponse(request.META['REMOTE_ADDR'])

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("threesidedcards.views.login"))


def login(request):

    if "user" in request.POST:
        user = User.objects.filter(username=request.POST["user"])
        if len(user) == 0:
            if not "131.215." in request.META['REMOTE_ADDR']:
                return render(request,"threesidedcards/login.html",{"notlocal": "true", "error": "Cannot create users from off-campus."})
            return render(request,"threesidedcards/login.html",{"create":request.POST["user"]})
        else:
            if user[0].is_staff:
                return HttpResponseRedirect("/flashcards/admin/")
            if user[0].is_superuser:
                return HttpResponseRedirect("/flashcards/admin/")

            password = defaultpass
            if not "131.215." in request.META['REMOTE_ADDR']:
                password = request.POST["password"]

            user = authenticate(username=user[0].username,password=password)
            if user is not None:
                auth_login(request,user)
                return HttpResponseRedirect(reverse("threesidedcards.views.home"))
            else:
                if not "131.215." in request.META['REMOTE_ADDR']:
                    return render(request,"threesidedcards/login.html",{"notlocal": "true", "error": "Authentication failed."})
                return render(request,"threesidedcards/login.html",{"error":"Authentication failed."})

    if "create" in request.POST:
        if not "131.215." in request.META['REMOTE_ADDR']:
            return render(request,"threesidedcards/login.html",{"notlocal": "true", "error": "Cannot create users from off-campus."})

        if request.POST["create"] == "No":
            return render(request,"threesidedcards/login.html")
        if request.POST["create"] == "Yes":
            try:
                user = User.objects.create_user(request.POST["createuser"],defaultemail,defaultpass)
                user.save()
            except IntegrityError:
                return render(request,"threesidedcards/login.html",{"error":"Could not create user."})

            @transaction.atomic
            def makeTriples(user):
                for triple in Triple.objects.all():
                    for direct in ['CP','PC','CE','EC','EP','PE']:
                        score = Score()
                        score.triple = triple
                        score.user = user
                        score.nexttime = datetime.datetime.now()
                        score.direction = direct
                        score.score = 0
                        score.save()

            makeTriples(user)

            user = authenticate(username=user.username,password=defaultpass)
            if user is not None:
                auth_login(request,user)
                return HttpResponseRedirect(reverse("threesidedcards.views.home"))
            else:
                return render(request,"threesidedcards/login.html",{"error":"Could not create user."})

    if not "131.215." in request.META['REMOTE_ADDR']:
        return render(request,"threesidedcards/login.html",{"notlocal": "true"})
    return render(request,"threesidedcards/login.html")


def home(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse("threesidedcards.views.login"))
        #return HttpResponse("Not logged in.")
    return render(request,"threesidedcards/home.html")


def getItems(request):
    items = Score.objects.filter(user=request.user,nexttime__lte=datetime.datetime.now())

    #if no items are found return the time when more will be available
    if len(items) == 0:
        items = Score.objects.filter(user=request.user).order_by("nexttime")
        return HttpResponse(json.dumps(items[0].nexttime,cls=DjangoJSONEncoder))


    for i in json.loads(request.GET['prev']):
        items = items.exclude(triple__pk=i)

    if len(items) == 0:
        items = Score.objects.filter(user=request.user,nexttime__lte=datetime.datetime.now())

    message = ""

    length = len(items)


    if "filter" in request.GET:
        newitems = items.filter(triple__chapter=request.GET["filter"])
        if (len(newitems) != 0):
            items = newitems
            message = "优先: Chapter " + request.GET["filter"] + ", "+str(len(newitems))+"个卡。"
        else:
            message = "No cards available for chapter "+request.GET["filter"]+"."


    if "quiz" in request.GET:
        newitems = items.filter(triple__quiz=True)
        if (len(newitems) != 0):
            items = newitems
            if "filter" in request.GET:
                message = "优先: Chapter " + request.GET["filter"] + " quiz, "+str(len(newitems))+"个卡。"
            else:
                message = "优先: All quizzes, "+str(len(newitems))+"个卡。"
        else:
            message = "No cards available for quiz"
            if "filter" in request.GET:
                message += " for chapter "+request.GET["filter"]
            message += "."

    chapters = []
    triples = Triple.objects.order_by("-chapter")
    while (len(triples) != 0):
        chapters.append(triples[0].chapter)
        triples = triples.exclude(chapter=triples[0].chapter)


    #if (datetime.date.today().weekday() < 2):
    #    #monday and tuesday prioritize the most recent chapter
    #    chapter = Triple.objects.order_by("-chapter")[0].chapter
    #    newitems = items.filter(triple__chapter=chapter)
    #    if (len(newitems) != 0):
    #        items = newitems
    #        message = "优先: Chapter " + str(chapter) + ", "+str(len(newitems))+"个卡。"

    choice = random.choice(items)

    if choice.direction[0] == "C":
        fromText = choice.triple.characters
        others = Triple.objects.filter(characters=fromText).exclude(pk=choice.triple.pk)
    elif choice.direction[0] == "P":
        fromText = choice.triple.pinyin
        others = Triple.objects.filter(pinyin=fromText).exclude(pk=choice.triple.pk)
    elif choice.direction[0] == "E":
        fromText = choice.triple.english
        others = Triple.objects.filter(english=fromText).exclude(pk=choice.triple.pk)

    alternatives = Score.objects.filter(direction=choice.direction, triple__in=others,user=request.user)
    combo = [choice] + list(alternatives)


    response = {
            "length": length,
            "current": [serializers.serialize("json",[elem]) for elem in combo],
            "message": message,
            "chapters": chapters
            }


    return HttpResponse(json.dumps(response))


def getTriples(request):
    triples = []
    for pk in json.loads(request.GET["pks"]):
        triples.append(Triple.objects.get(pk=pk))
    return HttpResponse(json.dumps([serializers.serialize("json",[triple]) for triple in triples]))


def newTime(score):
    now = datetime.datetime.now()
    if score == 0:
        return now + datetime.timedelta(minutes=1)
    if score == 1:
        return now + datetime.timedelta(hours=1)
    if score == 2:
        return now + datetime.timedelta(days=1)
    if score == 3:
        return now + datetime.timedelta(days=3.5)
    if score == 4:
        return now + datetime.timedelta(weeks=1)
    if score == 5:
        return now + datetime.timedelta(weeks=2)
    if score >= 6:
        return now + datetime.timedelta(months=1)



def submit(request):
    #for now just update the thing, later check correctness
    score = Score.objects.get(pk=request.GET["pk"])
    if "correct" in request.GET:
        score.score += 1
        score.nexttime = newTime(score.score)
    else:
        score.score = 0
        score.nexttime = newTime(0)
    score.save()
    return HttpResponse(serializers.serialize("json",[score.triple]))


def status(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse("threesidedcards.views.login"))

    return render(request,"threesidedcards/status.html")


def statusData(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse("threesidedcards.views.login"))

    if (request.user.is_staff or request.user.is_superuser or request.user.username == "wxyun"):
        datalist = []
        for user in User.objects.all():
            dataobject = {'name': user.username}
            dataobject["histogram"] = []
            count = 0
            scoretotal = 0
            for score in Score.objects.filter(user=user):
                scoretotal += score.score
                count += 1
                dataobject["histogram"].append({'score': score.score, 'direction':score.direction})
            if count == 0: dataobject["score"] = 0
            else: dataobject["score"] = round(scoretotal/count,2)
            datalist.append(dataobject)
        datalist.sort(key=lambda data: -data["score"])
    else:
        datalist = []
        dataobject = {'name': request.user.username}
        dataobject["histogram"] = []
        for score in Score.objects.filter(user=request.user):
            dataobject["histogram"].append({'score': score.score, 'direction':score.direction})
        datalist.append(dataobject)


    return HttpResponse(json.dumps(datalist))





