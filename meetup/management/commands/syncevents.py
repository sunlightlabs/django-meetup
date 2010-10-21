from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from meetup.api import MeetupClient
from meetup.models import Account, Event
import datetime

def parse_geo(geo):
    if not geo:
        return ''
    return "%0.6f" % geo

def parse_timestamp(ts):
    if not ts:
        return None
    try:
        return datetime.datetime.fromtimestamp(int(ts) / 1000)
    except ValueError, ve:
        print "!!! unable to convert timestamp %s" % ts
        raise ve

class Command(BaseCommand):
    args = '<container id>'
    help = 'Sync local events with those in container'
    
    def handle(self, *args, **options):
        
        for account in Account.objects.all():
            
            if not account.container_id:
                
                print "!!!\tno container ID found for key %s" % account.key
            
            else:
        
                client = MeetupClient(account.key)
        
                resp = client.container_events(account.container_id, extra_fields='rsvp_count')
        
                remote_ids = []
        
                for res in resp['results']:
            
                    event_id = str(res['id'])
            
                    try:
                        ev = Event.objects.get(pk=event_id, account=account)
                    except Event.DoesNotExist:
                        ev = Event(account=account)
                
                    ev.meetup_url = res['meetup_url']
                    ev.title = res.get('title', '')
                    ev.description = res.get('description', '')
                    ev.start_time = parse_timestamp(res.get('time', None))
                    ev.location = res.get('venue_name', '')
                    ev.address = res.get('address1', '')
                    ev.city = res.get('city', '')
                    ev.state = res.get('state', '')
                    ev.zipcode = res.get('zip', '')
                    ev.latitude = parse_geo(res.get('lat', None))
                    ev.longitude = parse_geo(res.get('lon', None))
                    ev.url = res.get('link', '')
                    ev.rsvp_count = res.get('rsvp_count', 0)
                    ev.timestamp = parse_timestamp(res.get('updated', None) or res['created'])
                    ev.status = res['status']
            
                    organizer = res.get('organizer', None)
                    if organizer:
                        ev.organizer_id = organizer['member_id']
                        ev.organizer_name = organizer['name']
            
                    # user defined fields
            
                    if ev.id:
                        print "* updated local event %s" % ev.pk
                    else:
                        ev.pk = event_id
                        print "* created local event %s" % ev.pk
            
                    ev.save(sync=False)    
                    
                    if res['status'] != 'past':    
                        remote_ids.append(event_id)
        
                local_ids = Event.objects.filter(account=account).exclude(status='past').values_list('id', flat=True)
                to_delete = set(local_ids) - set(remote_ids)
        
                for ev in Event.objects.filter(id__in=to_delete, account=account):
                    ev.delete()
            
                print "* deleted %s local events" % len(to_delete)
