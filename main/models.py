#!/usr/bin/python2
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

class Klasse(models.Model):
    kuerzel = models.CharField(max_length=5)

    def __unicode__(self):
        return self.kuerzel

class Schueler(models.Model):
    vorname = models.CharField(max_length=50)
    nachname = models.CharField(max_length=50)
    geburtstag = models.DateField()
    geschlecht = models.CharField(max_length=1,
        choices=(('M','Männlich'),('W','Weiblich')))

    klasse = models.ForeignKey(Klasse)

    def __unicode__(self):
        return "%s %s (%s)"%(self.vorname, self.nachname, self.klasse)

class Lehrer(models.Model):
    kuerzel = models.CharField(max_length=5)
    account = models.OneToOneField(User)

    def __unicode__(self):
        return self.kuerzel

class Kurs(models.Model):
    kuerzel = models.CharField(max_length=15)
    lehrer = models.ForeignKey(Lehrer)

    def __unicode__(self):
        return self.kuerzel

class Belegung(models.Model):
    kurs = models.ForeignKey(Kurs)
    schueler = models.ForeignKey(Schueler)

    bewertung = models.SmallIntegerField(blank=True, null=True)
    fehlstunden = models.SmallIntegerField(blank=True, null=True)

    def __unicode__(self):
        return u"%s € %s"%(self.schueler, self.kurs)


