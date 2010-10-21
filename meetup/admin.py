from django.contrib import admin
from meetup.models import Account,Event

class AccountAdmin(admin.ModelAdmin):
    list_display = ('key','description','container_id','sync')
    prepopulated_fields = {'slug': ('description',)}
admin.site.register(Account, AccountAdmin)

class EventAdmin(admin.ModelAdmin):
    list_display = ('id','status','start_time','location','city_state','short_description','organizer_name','rsvp_count')
    list_filter = ('status','account')
admin.site.register(Event, EventAdmin)