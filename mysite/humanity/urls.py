from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("person", views.people, name="people"),
    path("person/add", views.add_person, name="add_person"),
    path("person/add_bulk", views.bulk_add_people, name="bulk_add_people"),
    path("person/<int:person_id>", views.person, name="person"),
    path("person/<int:person_id>/edit", views.edit_person, name="edit_person"),
    path("person/<int:person_id>/delete", views.delete_person, name="delete_person"),
    path("person/<int:person_id>/call", views.call_person, name="call_person"),

    path("event", views.events, name="events"),
    path("event/add", views.add_event, name="add_event"),
    path("event/<int:event_id>", views.event, name="event"),
    path("event/<int:event_id>/edit", views.edit_event, name="edit_event"),
    path("event/<int:event_id>/add_attendee", views.add_attendee, name="add_attendee"),
    path("event/<int:event_id>/attendee", views.event_attendees, name="event_attendees"),
    path("event/<int:event_id>/attendee/<int:engagement_id>/edit", views.edit_event_attendee, name="edit_event_attendee"),
    path("event/<int:event_id>/attendee/<int:engagement_id>/delete", views.delete_event_attendee, name="delete_event_attendee"),

    path("call", views.calls, name="calls"),
    path("call/add", views.add_call, name="add_call"),

    path("seed", views.seed, name="seed"),
]