from django.views.generic.simple import direct_to_template

from main import models

def index(request):
    kurse = models.Kurs.objects.all()
    context = {
            'kurse': kurse,
    }
    return direct_to_template(request, "index.html", context)


