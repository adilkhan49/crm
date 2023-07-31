from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=255,unique=True)
    def __str__(self):
        return f"{self.name}"

class Person(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255,null=True,unique=True,blank=True)
    phone_number = models.CharField(max_length=25,null=True,blank=True)    
    region = models.ForeignKey(Region,on_delete=models.CASCADE,null=True,blank=True)
    location =  models.CharField(max_length=255,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

    @property
    def events_attended(self):
        return Person.objects.filter(
            engagement__person_id=self.id,
            engagement__engagement_role__name='Attendee')
    
    @property
    def num_events_attended(self):
        return len(self.events_attended)

    @property
    def calls_received(self):
        return Call.objects.filter(receiver=self.id)
    
    @property
    def num_calls(self):
        return len(self.calls_received)

    @property
    def is_called(self):
        return self.num_calls>0
    
class Role(models.Model):
    name = models.CharField(max_length=255,unique=True)

class PersonRole(models.Model):
    person = models.ForeignKey(Person,on_delete=models.CASCADE)
    role = models.ForeignKey(Role,on_delete=models.CASCADE)

class EventType(models.Model):
    name = models.CharField(max_length=255,unique=True)
    def __str__(self):
        return f"{self.name}"
    
class Event(models.Model):
    event_type = models.ForeignKey(EventType,on_delete=models.CASCADE)
    start_date = models.DateField()
    start_time = models.TimeField(blank=True,null=True)
    end_date = models.DateField(blank=True,null=True)
    end_time = models.TimeField(blank=True,null=True)
    location = models.CharField(max_length=255,blank=True,null=True)
    url = models.CharField(max_length=255,blank=True,null=True)
    organiser = models.ForeignKey(Person,on_delete=models.SET_NULL,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def invited(self):
        return Engagement.objects\
            .select_related('person')\
            .filter(
                event_id = self.id,
                engagement_role__name='Attendee')\
            .order_by('-created_at')
    
    @property
    def num_invited(self):
        return len(self.invited)

    @property
    def attended(self):
        return self.invited.filter(attended=True)

    @property
    def num_attended(self):
        return len(self.attended)
    
class EngagementRole(models.Model):
    name = models.CharField(max_length=255,unique=True)

class Engagement(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    person = models.ForeignKey(Person,on_delete=models.CASCADE)
    engagement_role = models.ForeignKey(EngagementRole,on_delete=models.CASCADE)
    invited = models.BooleanField(null=True,blank=True,default=True)
    confirmed = models.BooleanField(null=True,blank=True)
    attended = models.BooleanField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = (('event', 'person'))

class CallOutcome(models.Model):
    name = models.CharField(max_length=255,unique=True)
    def __str__(self):
        return f"{self.name}"
    
class CallReason(models.Model):
    name = models.CharField(max_length=255,unique=True)
    def __str__(self):
        return f"{self.name}"
    
class Call(models.Model):
    caller = models.ForeignKey(Person,on_delete=models.CASCADE,related_name='called')
    receiver = models.ForeignKey(Person,on_delete=models.CASCADE,related_name='received')
    reason = models.ForeignKey(CallReason,on_delete=models.CASCADE,null=True,blank=True)
    outcome = models.ForeignKey(CallOutcome,on_delete=models.CASCADE,null=True,blank=True)
    call_time = models.DateTimeField()
    notes = models.CharField(max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Interest(models.Model):
    name = models.CharField(max_length=255,unique=True)

class PersonInterest(models.Model):
    person = models.ForeignKey(Person,on_delete=models.CASCADE)
    interest = models.ForeignKey(Interest,on_delete=models.CASCADE)
    class Meta:
        unique_together = (('person', 'interest'))

class Tag(models.Model):
    name = models.CharField(max_length=255,unique=True)

class PersonTag(models.Model):
    person = models.ForeignKey(Person,on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE)
    class Meta:
        unique_together = (('person', 'tag'))
      
