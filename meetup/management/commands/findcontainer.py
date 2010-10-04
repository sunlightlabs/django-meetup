from django.conf import settings
from django.core.management.base import LabelCommand, CommandError
from meetup.api import MeetupClient

class Command(LabelCommand):
    args = '<container name>'
    help = 'Search for container IDs'
    
    def handle_label(self, label, **options):
        
        print "Searching for '%s'" % label
        
        key = getattr(settings, 'MEETUP_KEY', None)
        if not key:
            raise CommandError('MEETUP_KEY is not found in settings.py')
        
        client = MeetupClient(key)
        resp = client.find_containers(label)
        
        if resp['meta']['count'] == 0:
        
            print "-- no results found --"
            
        else:
        
            for res in resp['results']:
                cont_id = str(res['id']).ljust(5, ' ')
                print "%s %s" % (cont_id, res['name'])