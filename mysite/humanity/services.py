from .models import Region, Person, EventType, EngagementRole, CallOutcome, CallReason
from django.db import IntegrityError

def seed_db():

    event_types = ['Mobilisation']
    regions = ['Scotland','Wales','East of England',
               'London','Midlands','North England','South East']
    engagement_roles = ['Speaker','Attendee']
    call_reasons = ['Sign up','Mobilise','Invite']
    call_outcomes = ['Did Not Answer','Call Back','Answered']

    people = [
        {
            'first_name': 'Adil',
            'last_name': 'Khan',
            'email': 'hexamadoodle@gmail.com',
            'region': 'London',
         },        {
            'first_name': 'Jacky',
            'last_name': 'Mashallah',
            'email': 'jm@scottie.com',
            'region': 'Scotland',
         },
        {
            'first_name': 'Weslie',
            'last_name': 'Norbit',
            'email': 'rishidishi@zoo.com',
            'region': 'Wales',
         },
        {
            'first_name': 'McKinsie',
            'last_name': 'Throwdown',
            'email': 'benkings@barkingparish.com',
            'region': 'London',
         },
    ]

    for region in regions:
        x,created = Region.objects.get_or_create(name=region)
        if created:
            x.save()

    for i,person in enumerate(people):
        try:
            person['region'] = Region.objects.get(name=person['region'])
            x,created = Person.objects.get_or_create(**person)
            if created:
                x.save()
        except IntegrityError as e:
             pass

    for event_type in event_types:
            x,created = EventType.objects.get_or_create(name=event_type)
            if created:
                x.save()

    for role in engagement_roles:
        x,created = EngagementRole.objects.get_or_create(name=role)
        if created:
            x.save()

    for reason in call_reasons:
        x,created = CallReason.objects.get_or_create(name=reason)
        if created:
            x.save()

    for outcome in call_outcomes:
        x,created = CallOutcome.objects.get_or_create(name=outcome)
        if created:
            x.save()

    

    