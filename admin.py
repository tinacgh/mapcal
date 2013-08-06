from django.contrib import admin
from mapcal.models import Appt, Marker, Tag

class MarkerInline(admin.StackedInline):
    model = Marker
    extra = 1

class ApptAdmin(admin.ModelAdmin):
    inlines = [MarkerInline]

admin.site.register(Appt, ApptAdmin)
admin.site.register(Marker)
admin.site.register(Tag)
