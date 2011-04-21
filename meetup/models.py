from django.conf import settings
from django.db import models
from meetup.api import MeetupClient
import datetime

STATUSES = [(s, s) for s in ('past','pending','upcoming')]
API_KEY = getattr(settings, 'MEETUP_KEY', None)

class Account(models.Model):
    key = models.CharField(max_length=128)
    description = models.CharField(max_length=128)
    slug = models.SlugField()
    container_id = models.CharField(max_length=16, blank=True)
    sync = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.slug
    
    def past_events(self):
        return self.events.filter(status='past')
    
    def upcoming_events(self):
        return self.events.filter(status='upcoming')

class EventManager(models.Manager):
    def past(self):
        return Event.objects.filter(status='past')
    def upcoming(self):
        return Event.objects.filter(status='upcoming')

class Event(models.Model):
    
    objects = EventManager()
    
    account = models.ForeignKey(Account, related_name="events")
    
    # Meetup.com fields
    id = models.CharField(max_length=255, primary_key=True)
    meetup_url = models.URLField(verify_exists=False)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=64, blank=True)
    state = models.CharField(max_length=64, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    latitude = models.CharField(max_length=16, blank=True)
    longitude = models.CharField(max_length=16, blank=True)
    url = models.URLField(verify_exists=False, max_length=255, blank=True)
    rsvp_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField()
    status = models.CharField(max_length=16, choices=STATUSES)
    organizer_id = models.CharField(max_length=32, blank=True)
    organizer_name = models.CharField(max_length=128, blank=True)
    
    # user defined fields
    # none for now, add tags later
    
    class Meta:
        ordering = ('start_time',)
    
    def __unicode__(self):
        return self.pk
    
    def save(self, sync=True, **kwargs):
        super(Event, self).save(**kwargs)
        # if sync:
        #     api_client = MeetupClient(self.account.key)
        #     api_client.update_event(self.pk, udf_category=self.category)
    
    def city_state(self):
        if self.city:
            if self.state:
                return "%s, %s" % (self.city, self.state)
            else:
                return self.city
        elif self.state:
            return self.state
        else:
            return ''
    
    def short_description(self, length=64):
        if len(self.description) > length:
            desc = self.description[:length]
            if desc.endswith(' '):
                desc = desc[:-1]
            return desc + '...'
        return self.description