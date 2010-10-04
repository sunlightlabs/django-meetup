from django.contrib import admin
from meetup.models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ('id','category','status','start_time','location','city_state','short_description','organizer_name','rsvp_count')
    list_filter = ('status','category')

admin.site.register(Event, EventAdmin)