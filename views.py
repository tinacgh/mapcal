# Create your views here.
from django.http import HttpResponse

from mapcal.models import Appt, Marker, Tag

def queryset_str(qs):
    return " ".join([str(i) for i in qs])

def bytag(request):
    appts_work = Appt.objects.filter(tags__name="work")
    appts_fun = Appt.objects.filter(tags__name="fun")
    resp = queryset_str(appts_work) + " | " + queryset_str(appts_fun)
    return HttpResponse(resp)
