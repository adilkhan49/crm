from django.contrib import admin
from .models import Person,Region,EventType,Event

class PersonAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name","email"]

class EventAdmin(admin.ModelAdmin):
    list_display =[    
        "event_type",
        "start_date",
        "start_time",
        "end_date",
        "end_time",
        "location",
        "url",
        ]
    
admin.site.register(Region)
admin.site.register(EventType)
admin.site.register(Person,PersonAdmin)
admin.site.register(Event,EventAdmin)