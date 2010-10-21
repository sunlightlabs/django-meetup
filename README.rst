=============
django-meetup
=============

A very basic client for creating a local cache of Meetup.com/everywhere events.


Management Commands
===================

findcontainer <search>
	Find IDs of containers that match <search>. Requires MEETUP_KEY setting.

syncevents
	Make a local copy of existing container events. Requires Account instances with key and container_id settings.


API Client Methods
==================

	from meetup.api import MeetupClient

	client = MeetupClient(meetup_key)

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