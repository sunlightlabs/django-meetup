from urllib import urlencode
from urllib2 import urlopen
try:
    import json
except ImportError:
    import simplejson as json

class MeetupClient(object):
    
    def __init__(self, key):
        self.key = key
    
    def _invoke(self, endpoint, params=None, method='GET'):
        
        params = params.copy() if params else {}
        params['key'] = self.key
        params['page'] = 1000
        
        url = "http://api.meetup.com/ew/%s" % endpoint
        
        if method == 'GET':
            return self._get(url, params)
        elif method == 'POST':
            return self._post(url, params)
    
    def _get(self, url, params):
        url = "%s?%s" % (url, urlencode(params))
        return json.load(urlopen(url))
        
    def _post(self, url, params):
        return json.load(urlopen(url, urlencode(params)))
    
    def find_containers(self, name):
        return self._invoke('containers', {'urlname': name})
    
    def container_events(self, container_id, extra_fields=None):
        params = {'container_id': container_id}
        if extra_fields:
            params['fields'] = extra_fields
        return self._invoke('events', params)
    
    def update_event(self, event_id, **params):
        return self._invoke('event/%s' % event_id, params, method='POST')