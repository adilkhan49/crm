from .models import Region, Person, EventType, EngagementRole, CallOutcome, CallReason
from django.db import IntegrityError

import pandas as pd
import io

def update_attrs(instance, **kwargs):
    """ Updates model instance attributes and saves the instance
    :param instance: any Model instance
    :param kwargs: dict with attributes
    :return: updated instance, reloaded from database
    """
    instance_pk = instance.pk
    for key, value in kwargs.items():
        if hasattr(instance, key):
            setattr(instance, key, value)
        else:
            raise KeyError("Failed to update non existing attribute {}.{}".format(
                instance.__class__.__name__, key
            ))
    instance.save(force_update=True)
    return instance.__class__.objects.get(pk=instance_pk)

    
def upsert_people(file_obj):
    df = pd.read_csv(io.StringIO(file_obj.read().decode('utf-8')), delimiter=',')
    df = df[df['email'].notna()]
    created,updated = 0,0
    for i,person in df.iterrows():
        person = person.dropna()
        p = Person.objects.filter(email=person['email']).first()
        if p:
            update_attrs(p,**person)
            print(f'Updated {p.email}')
            updated += 1
        else:
            p,is_created = Person.objects.get_or_create(**person)
            p.save()
            print(f'Added {p.email}')
            created += 1
    return {"created": created, "updated": updated }
