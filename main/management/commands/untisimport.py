
# importiert kursdaten aus untis' GPU????.TXT-dateien

from django.core.management.base import BaseCommand, CommandError
from main.models import *
from django.contrib.auth.models import User

from os import path, stat
import csv, re, sys

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
        self.fd = open(dateiname, "rb")
        self.size = stat(dateiname).st_size
        self.reader = csv.reader(self.fd)
        self.lastnum = 0

    def getFortschritt(self):
        return self.fd.tell() / float(self.size)

    def next(self):
        if self.getFortschritt()*80 > self.lastnum:
            self.lastnum += 1
            sys.stdout.write("#")
            sys.stdout.flush()
        try:
            return [s.decode("latin1") for s in self.reader.next()]
        except StopIteration:
            print "#" * (80 - self.lastnum)
            raise

    def __iter__(self):
        return self

def loescheAltesZeug():
    print "Loesche alte Daten..."
    Belegung.objects.all().delete()
    Kurs.objects.all().delete()
    Lehrer.objects.all().delete()
    Schueler.objects.all().delete()
    Klasse.objects.all().delete()
    print

def importiereKlassen(datei):
    print "Importiere Klassen..."
    for data in GPULeser(datei):
        neueKlasse = Klasse()
        neueKlasse.kuerzel = data[0]
        neueKlasse.save()
    print

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
    print

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
    print

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
    print

def importiereBelegungen(datei):
    print "Importiere Belegungen..."
    for data in GPULeser(datei):
        neueBelegung = Belegung()
        neueBelegung.kurs = Kurs.objects.get(untisid__exact = int(data[1]))
        neueBelegung.schueler = Schueler.objects.get(untisid__exact = data[0])
        neueBelegung.save()
    print

