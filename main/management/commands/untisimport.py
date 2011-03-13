
# importiert kursdaten aus untis' GPU????.TXT-dateien

from django.core.management.base import BaseCommand, CommandError
from main.models import *
from django.contrib.auth.models import User

from os import path
import csv, re

class Command(BaseCommand):
    args = '<Pfad zum Ordner, in dem die GPU-Dateien liegen>'
    help = 'Importiert die Kursdaten aus GPU-Exportdateien der Software Untis'

    def handle(self, ordner, **keyargs):
        loescheAltesZeug()
        importiereKlassen(    path.join(ordner, "GPU003.TXT"))
        importiereLehrer(     path.join(ordner, "GPU004.TXT"))
        importiereSchueler(   path.join(ordner, "GPU010.TXT"))
        importiereKurse(      path.join(ordner, "GPU002.TXT"),
                              path.join(ordner, "GPU006.TXT"))
        importiereBelegungen( path.join(ordner, "GPU015.TXT"))
        print "Fertig."


class GPULeser:
    def __init__(self, dateiname):
       self.reader = csv.reader(open(dateiname, "rb"))

    def next(self):
        return [s.decode("latin1") for s in self.reader.next()]

    def __iter__(self):
        return self

def loescheAltesZeug():
    print "Loesche alte Daten..."
    Belegung.objects.all().delete()
    Kurs.objects.all().delete()
    Lehrer.objects.all().delete()
    Schueler.objects.all().delete()
    Klasse.objects.all().delete()

def importiereKlassen(datei):
    print "Importiere Klassen..."
    for data in GPULeser(datei):
        neueKlasse = Klasse()
        neueKlasse.kuerzel = data[0]
        neueKlasse.save()

def importiereLehrer(datei):
    print "Importiere Lehrer..."
    for data in GPULeser(datei):
        neuerLehrer = Lehrer()
        neuerLehrer.kuerzel = data[0]

        username = data[0].lower()
        try:
            neuerAccount = User.objects.get(username__exact=username)
        except User.DoesNotExist:
            neuerAccount = User.objects.create_user(username, 'inval')

        neuerLehrer.account = neuerAccount
        neuerLehrer.save()

def importiereSchueler(datei):
    print "Importiere Schueler..."
    for data in GPULeser(datei):
        neuerSchueler = Schueler()
        neuerSchueler.untisid = data[0]
        neuerSchueler.vorname = data[7]
        neuerSchueler.nachname = re.sub(r"(\+|\(.\))+$", "", data[0])
        if (data[12]):
            neuerSchueler.geburtstag = re.sub(
                    r"(....)(..)(..)", r"\1-\2-\3", data[12])
        neuerSchueler.geschlecht = "M"  if  data[6] == "M"  else  "W"
        neuerSchueler.klasse = Klasse.objects.get(kuerzel__exact = data[9])
        neuerSchueler.save()

def importiereKurse(datei, bezeichnungsdatei):
    print "Importiere Kurse..."
    for data in GPULeser(datei):
        untisid = int(data[0])
        try:
            Kurs.objects.get(untisid__exact = untisid)
        except Kurs.DoesNotExist:
            neuerKurs = Kurs()
            neuerKurs.untisid = untisid
            neuerKurs.kuerzel = data[6]
            try:
                neuerKurs.lehrer = Lehrer.objects.get(kuerzel__exact = data[5])
            except Lehrer.DoesNotExist:
                pass
            neuerKurs.save()

def importiereBelegungen(datei):
    print "Importiere Belegungen..."
    for data in GPULeser(datei):
        neueBelegung = Belegung()
        neueBelegung.kurs = Kurs.objects.get(untisid__exact = int(data[1]))
        neueBelegung.schueler = Schueler.objects.get(untisid__exact = data[0])
        neueBelegung.save()

