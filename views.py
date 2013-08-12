# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from mapcal.models import Appt, Marker, Tag
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

def name_id(obj):
    return str(obj) + " " + str(obj.id)

def queryset_str(qs):
    return " ".join([name_id(i) for i in qs])

@login_required
def listappts(request):
    appts = Appt.objects.filter(user__username=request.user.username).order_by('time').filter(time__gte=timezone.now())
    return render(request, 'mapcal/listappts.html', { 'appts': appts })

@login_required
def listallappts(request):
    appts = Appt.objects.filter(user__username=request.user.username).order_by('time')
    return render(request, 'mapcal/listappts.html', { 'appts': appts })

@login_required
def alltags(request):
    tags = Tag.objects.filter(appt__user__username=request.user.username).distinct().order_by('name')
    return render(request, 'mapcal/alltags.html', { 'tags': tags })

@login_required
def bytag(request, tag_id):
    appts_by_user = Appt.objects.filter(user__username=request.user.username)
    appts_tag = appts_by_user.filter(tags__id=tag_id).order_by('time')
    tag = get_object_or_404(Tag, pk=tag_id)
    return render(request, 'mapcal/bytag.html', { 'appts': appts_tag, 'tag': tag })

@login_required
def detail(request, appt_id):
    appt = get_object_or_404(Appt, pk=appt_id)
    if appt.user.username == request.user.username:
        return render(request, 'mapcal/detail.html', {'appt': appt })
    else:
        return HttpResponse("Not your appt")

@login_required
def edit(request, appt_id):
    appt = get_object_or_404(Appt, pk=appt_id)
    tags = appt.tags.all()
    tag1 = ""
    tag2 = ""
    tag3 = ""
    if len(tags) > 0:
        tag1 = tags[0]
        if len(tags) > 1:
            tag2 = tags[1]
            if len(tags) > 2:
                tag3 = tags[2]
    return render(request, 'mapcal/addform.html', { 'appt': appt, 'tag1': tag1, 'tag2': tag2, 'tag3': tag3 })
    
@login_required
def add(request):
    if request.method == 'POST':
        resp = ""
        req_del_id = request.POST.get('del_id', '')
        req_desc = request.POST.get('desc', '')
        req_notes = request.POST.get('notes', '')
        
        req_tag1 = request.POST.get('tag1', 'untagged')
        req_tag2 = request.POST.get('tag2', '')
        req_tag3 = request.POST.get('tag3', '')
        
        req_nummarkers = request.POST.get('nummarkers', '')
        req_markercoords = request.POST.get('markercoords', '')

        req_ymd = request.POST.get('ymd', '')
        req_time = request.POST.get('time', '12:00')

        user = User.objects.get(username=request.user.username)
        
# delete existing entry if coming from edit
        if req_del_id != "":
            appt = Appt.objects.get(pk=int(req_del_id))
            if appt.user.username == request.user.username:
                appt.delete()

        if req_ymd == "":
            req_ymd = datetime.now().strftime("%Y-%m-%d")

        if req_tag1 == "":
            req_tag1 = "untagged"

        if req_time == "":
            req_time = "12:00"

        year, month, day = map(int, req_ymd.split("-"))
        hour, mins = map(int, req_time.split(":"))
        apptdate = datetime(year, month, day, hour, mins)

        newappt = Appt(user=user, time=apptdate,
                       desc=req_desc, notes=req_notes)
        newappt.save()
        
        if req_tag1 != "":
            try:
                tag1 = Tag.objects.get(name=req_tag1)
            except Tag.DoesNotExist:
                tag1 = Tag(name=req_tag1)
                tag1.save()
            newappt.tags.add(tag1)

        if req_tag2 != "":
            try:
                tag2 = Tag.objects.get(name=req_tag2)
            except Tag.DoesNotExist:
                tag2 = Tag(name=req_tag2)
                tag2.save()
            newappt.tags.add(tag2)

        if req_tag3 != "":
            try:
                tag3 = Tag.objects.get(name=req_tag3)
            except Tag.DoesNotExist:
                tag3 = Tag(name=req_tag3)
                tag3.save()
            newappt.tags.add(tag3)

        
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

@login_required
def delete_appt(request):
    if request.method == 'POST':
        req_id = request.POST.get('apptid', '')
        appt = Appt.objects.get(pk=req_id)
        if appt.user.username == request.user.username:
            appt.delete()
    return HttpResponseRedirect('/mapcal/')

def mapcal_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/mapcal/')
    else:
        return HttpResponse('User not found or password incorrect. <a href="/mapcal/accounts/login/">try again</a>')

def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')
