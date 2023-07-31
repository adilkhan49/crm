from django import forms
from .models import Person, Event, Call, Engagement
from django.contrib.admin.widgets import FilteredSelectMultiple

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "region",
            "location",
        )
        widgets = {
            'email': forms.EmailInput()
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            "event_type",
            "start_date",
            "start_time",
            "end_date",
            "end_time",
            "location",
            "url",
            "organiser",
        )
        widgets = {
            'start_date': forms.DateInput(attrs={'format': 'yyyy-mm-dd','type':'date'}),
            'end_date': forms.DateInput(attrs={'format': 'yyyy-mm-dd','type':'date'}),
            'start_time': forms.TimeInput(attrs={'type':'time'}),
            'end_time': forms.TimeInput(attrs={'type':'time'}),
        }

class AttendanceForm(forms.Form):
    attendee = forms.ModelChoiceField(
        queryset = Person.objects.all(),
    )

class CallForm(forms.ModelForm):
    class Meta:
        model = Call
        fields = (
            "receiver",
            "call_time",
            "caller",
            "reason",
            "outcome",
            "notes",
        )
        widgets = {
            'call_time': forms.DateTimeInput(format=('%Y-%m-%dT%H:%M'), attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea()
        }

class EngagementFormInvite(forms.ModelForm):
    class Meta:
        model = Engagement
        fields = (
            "invited",
        )

class EngagementFormConfirmed(forms.ModelForm):
    class Meta:
        model = Engagement
        fields = (
            "confirmed",
        )

class EngagementFormAttended(forms.ModelForm):
    class Meta:
        model = Engagement
        fields = (
            "attended",
        )