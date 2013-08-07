from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=60)
    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name

class Appt(models.Model):
    user = models.ForeignKey(User)
    time = models.DateTimeField('time and date')
    desc = models.CharField(max_length=100)
    notes = models.CharField(max_length=300, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    def __str__(self):
        return self.desc
    def __unicode__(self):
        return self.desc

class Marker(models.Model):
    appt = models.ForeignKey(Appt)
    lat = models.FloatField()
    lng = models.FloatField()
    desc = models.CharField(max_length=60, blank=True)
    def __str__(self):
        return "%s: %f, %f" % (self.desc, self.lat, self.lng)
    def __unicode__(self):
        return "%s: %f, %f" % (self.desc, self.lat, self.lng)
