from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.exceptions import ObjectDoesNotExist


class Triple(models.Model):
    pinyin = models.CharField(max_length=400)
    characters = models.CharField(max_length=400)
    english = models.CharField(max_length=400)
    chapter = models.IntegerField()
    quiz = models.BooleanField()

    def __str__(self):
        return self.pinyin +" - "+ self.characters +" - "+ self.english


    def save(self,*args,**kwargs):
        super(Triple,self).save(*args,**kwargs)
        for user in User.objects.all():
            for direct in ['CP','PC','CE','EC','EP','PE']:
                score = Score.objects.filter(user=user,triple=self,direction=direct)
                if len(score) == 0:
                    score = Score()
                    score.triple = self
                    score.user = user
                    score.nexttime = datetime.datetime.now()
                    score.direction = direct
                    score.score = 0
                    score.save()



class Score(models.Model):
    triple = models.ForeignKey(Triple)
    user = models.ForeignKey(User)
    score = models.FloatField()
    nexttime = models.DateTimeField()
    DIRECTIONS = (
        ('CP', 'Characters to Pīnyīn'),
        ('PC', 'Pīnyīn to Characters'),
        ('CE', 'Characters to English'),
        ('EC', 'English to Characters'),
        ('EP', 'English to Pīnyīn'),
        ('PE', 'Pīnyīn to Characters'),
    )
    direction = models.CharField(max_length=2,choices=DIRECTIONS)

    def __str__(self):
        string = self.user.username + ": "
        for i in [0,1]:
            if self.direction[i] == 'C':
                string += self.triple.characters
            if self.direction[i] == 'P':
                string += self.triple.pinyin
            if self.direction[i] == 'E':
                string += self.triple.english
            if i == 0: string += " to "
        string += " - Score: "+str(self.score)
        return string


