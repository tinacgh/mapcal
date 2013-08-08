# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from mapcal.models import Appt, Marker, Tag
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

def name_id(obj):
    return str(obj) + " " + str(obj.id)

def queryset_str(qs):
    return " ".join([name_id(i) for i in qs])

def listappts(request):
    appts = Appt.objects.order_by('time').filter(time__gte=timezone.now())
    return render(request, 'mapcal/listappts.html', { 'appts': appts })

def listallappts(request):
    appts = Appt.objects.order_by('time')
    return render(request, 'mapcal/listappts.html', { 'appts': appts })

def bytag(request):
    appts_by_user = Appt.objects.filter(user__username="admin")
    appts_work = appts_by_user.filter(tags__name="work")
    appts_fun = Appt.objects.filter(tags__name="fun")
    resp = queryset_str(appts_work) + " | " + queryset_str(appts_fun)
    return HttpResponse(resp)

def detail(request, appt_id):
    appt = get_object_or_404(Appt, pk=appt_id)
    return render(request, 'mapcal/detail.html', {'appt': appt})

def add(request):
    if request.method == 'POST':
        resp = ""
        req_username = request.POST.get('username', '')
        req_desc = request.POST.get('desc', '')
        req_notes = request.POST.get('notes', '')
        
        req_tag1 = request.POST.get('tag1', 'untagged')
        req_tag2 = request.POST.get('tag2', '')
        req_tag3 = request.POST.get('tag3', '')
        
        req_nummarkers = request.POST.get('nummarkers', '')
        req_markercoords = request.POST.get('markercoords', '')

        req_ymd = request.POST.get('ymd', '')
        req_time = request.POST.get('time', '12:00')

        user = User.objects.get(username=req_username)

        if req_ymd == "":
            req_ymd = datetime.now().strftime("%Y-%m-%d")

        if req_tag1 == "":
            req_tag1 = "untagged"

        if req_time == "":
            req_time = "12:00"

        if req_tag1 != "":
            try:
                tag1 = Tag.objects.get(name=req_tag1)
            except Tag.DoesNotExist:
                tag1 = Tag(name=req_tag1)
                tag1.save()

        year, month, day = map(int, req_ymd.split("-"))
        hour, mins = map(int, req_time.split(":"))
        apptdate = datetime(year, month, day, hour, mins)

        newappt = Appt(user=user, time=apptdate,
                       desc=req_desc, notes=req_notes)
        newappt.save()
        newappt.tags.add(tag1)
        
        
        resp += "tag1 id: " + str(tag1.id) + " "
        
        resp += req_nummarkers + "<br>"

        markers = req_markercoords.split(";")[0:-1]
        for marker in markers:
            coords = marker.split(",")
            resp += "Lat: " + coords[0] + ", "
            resp += "Lng: " + coords[1] + "<br>"
            newappt.marker_set.create(lat=coords[0], lng=coords[1], desc="addpost")
        
        resp += '<p><a href="/mapcal/add">add new appt</a></p>'
        
        return HttpResponseRedirect('/mapcal/'+str(newappt.id)+'/detail/')
    return render(request, 'mapcal/addform.html')

def delete_appt(request):
    if request.method == 'POST':
        req_id = request.POST.get('apptid', '')
        appt = Appt.objects.get(pk=req_id)
        appt.delete()
    return HttpResponseRedirect('/mapcal/')
