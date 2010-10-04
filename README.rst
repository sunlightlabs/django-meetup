=============
django-meetup
=============

A very basic client for creating a local cache of Meetup.com/everywhere events.


Settings
========

MEETUP_KEY
	API key

MEETUP_CONTAINER
	ID of container from which events will be pulled

MEETUP_CATEGORIES
	list of categories that can be associated with events


Management Commands
===================

findcontainer <search>
	Find IDs of containers that match <search>. Requires MEETUP_KEY setting.

syncevents
	Make a local copy of existing container events. Requires MEETUP_KEY and MEETUP_CONTAINER settings.


API Client Methods
==================

	from django.conf import settings
	from meetup.api import MeetupClient

	client = MeetupClient(settings.MEETUP_KEY)

client.find_containers(name)
----------------------------

Find containers that match the specified name.

client.container_events(container_id, extra_fields)
---------------------------------------------------

Load events from meetup.com.

container_id
	ID of container (use find_containers to get ID from name)
	
extra_fields
	Comma-separated list of extra and user defined fields to fetch.

client.update_event(event_id, \*\*params)
-----------------------------------------

Update parameters on event.

event_id
	ID of event to edit.

params
	Attributes to be updated. Allowed parameters: http://www.meetup.com/meetup_api/everywhere/#event_edit