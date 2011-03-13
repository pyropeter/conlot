#!/usr/bin/python2
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

class Klasse(models.Model):
    kuerzel = models.CharField(max_length=5, unique=True)

    def __unicode__(self):
        return self.kuerzel

class Schueler(models.Model):
    vorname = models.CharField(max_length=50)
    nachname = models.CharField(max_length=50)
    geburtstag = models.DateField(blank=True, null=True)
    geschlecht = models.CharField(max_length=1,
        choices=(('M','Männlich'),('W','Weiblich')))

    untisid = models.CharField(max_length=50, unique=True)

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
    lehrer = models.ForeignKey(Lehrer, blank=True, null=True)

    untisid = models.IntegerField(unique=True)

    def __unicode__(self):
        return "%s (%s)"%(self.kuerzel, self.lehrer)

class Belegung(models.Model):
    kurs = models.ForeignKey(Kurs)
    schueler = models.ForeignKey(Schueler)

    bewertung = models.SmallIntegerField(blank=True, null=True)
    fehlstunden = models.SmallIntegerField(blank=True, null=True)

    def __unicode__(self):
        return u"%s € %s"%(self.schueler, self.kurs)


