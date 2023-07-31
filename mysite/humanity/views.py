from django.shortcuts import render,get_object_or_404, HttpResponseRedirect,reverse
from django.http import HttpResponse
from django.contrib import messages
from django.utils.timezone import localtime

from .models import Person, Event, Engagement, EngagementRole, Call
from .seed import seed_db
from .services import upsert_people,update_attrs
from .forms import PersonForm, EventForm, AttendanceForm, CallForm, EngagementFormInvite, EngagementFormConfirmed, EngagementFormAttended


def index(request):
    context = {
        'num_people': Person.objects.count(),
        'num_events': Event.objects.count(),
        'num_contacted': Call.objects.values_list('receiver').distinct().count()
    }
    return render(request, "humanity/index.html", context)

def people(request):
    context = {'people':  Person.objects.all().order_by('-updated_at')}
    return render(request, "humanity/people.html", context)

def person(request,person_id):
    context = {'person':  get_object_or_404(Person,pk=person_id)}
    return render(request, "humanity/person.html", context)

def seed(request):
    seed_db()
    return HttpResponse("Ingested Seed Data")

def add_person(request):
    if request.method == "POST":
        form = PersonForm(request.POST)
        if form.is_valid():
            p = Person(**form.cleaned_data)
            p.save()
            return HttpResponseRedirect(reverse('people'))
    else:
        form = PersonForm()
    return render(request, "humanity/add_person.html", {"form": form})

def bulk_add_people(request):
    if request.method == "POST":
        file_obj = request.FILES['file']
        if not file_obj.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
        res = upsert_people(file_obj)
        messages.success(request, res)
        return render(request, "humanity/bulk_load_success.html")
    return render(request, "humanity/bulk_add_people.html")

def delete_person(request,person_id):
    p = get_object_or_404(Person,pk=person_id)
    p.delete()
    return HttpResponseRedirect(reverse('people'))

def edit_person(request,person_id):
    p = get_object_or_404(Person,pk=person_id)
    form = PersonForm(instance=p)
    if request.method == "POST":    
        form = PersonForm(request.POST,instance=p)
        if form.is_valid():
            update_attrs(p,**form.cleaned_data)
            return HttpResponseRedirect(reverse('person',kwargs={"person_id": person_id}))

    else:
        form = PersonForm(instance=p)
    return render(request, "humanity/add_person.html", {"form": form})

def events(request):
    context = {'events':  Event.objects.all().order_by('-updated_at')}
    return render(request, "humanity/events.html", context)

def event(request,event_id):
    context = {'event':  get_object_or_404(Event,pk=event_id)}
    return render(request, "humanity/event.html", context)

def add_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            e = Event(**form.cleaned_data)
            e.save()
            print('redirect')
            return HttpResponseRedirect(reverse('events'))

    else:
        form = EventForm()
    return render(request, "humanity/add_event.html", {"form": form})


def edit_event(request,event_id):
    e = get_object_or_404(Event,pk=event_id)
    form = EventForm(instance=e)
    if request.method == "POST":    
        form = EventForm(request.POST,instance=e)
        if form.is_valid():
            update_attrs(e,**form.cleaned_data)
            return HttpResponseRedirect(reverse('event',kwargs={"event_id": event_id}))
    else:
        form = EventForm(instance=e)
    return render(request, "humanity/add_person.html", {"form": form})

def add_attendee(request,event_id):
    if request.method == "POST":
        e = get_object_or_404(Event,pk=event_id)
        form = AttendanceForm(request.POST)
        if form.is_valid():
            print('valid')
            person_id = form.cleaned_data['attendee'].id
            engagement_role = EngagementRole.objects.filter(name='Attendee').first()
            engagement = Engagement.objects.create(
                person_id = person_id,
                event_id = event_id,
                engagement_role = engagement_role
            )
            engagement.save()
            # p = Person(**form.cleaned_data)
            # p.save()
            return HttpResponseRedirect(reverse('event_attendees',kwargs={"event_id": event_id}))
        else:
            print(form.errors)
    else:
        form = AttendanceForm()
    return render(request, "humanity/add_attendee.html", {"form": form})

def event_attendees(request,event_id):
    context = {
        'event': get_object_or_404(Event,pk=event_id)}
    return render(request, "humanity/event_attendees.html", context)

def calls(request):
    context = {'calls':  Call.objects.all().order_by('-updated_at')}
    return render(request, "humanity/calls.html", context)


def add_call(request):
    if request.method == "POST":
        form = CallForm(request.POST)
        if form.is_valid():
            c = Call(**form.cleaned_data)
            c.save()
            print('redirect')
            return HttpResponseRedirect(reverse('calls'))
    else:
        
        form = CallForm(initial={'call_time':localtime()})
    return render(request, "humanity/add_call.html", {"form": form})

def edit_event_attendee(request,event_id,engagement_id):
    if request.method == "POST":
        print(request.POST)
        e = get_object_or_404(Engagement,pk=engagement_id)
        if 'invited' in request.POST.keys():
            form = EngagementFormInvite(request.POST)
        elif 'confirmed' in request.POST.keys():
            form = EngagementFormConfirmed(request.POST)
        elif 'attended' in request.POST.keys():
            form = EngagementFormAttended(request.POST)
        if form.is_valid():
            print('valid')
            print(form.cleaned_data)
            update_attrs(e,**form.cleaned_data)
            return HttpResponseRedirect(reverse('event_attendees',kwargs={"event_id": event_id}))
    return HttpResponse(200)


def delete_event_attendee(request,event_id,engagement_id):
    e = get_object_or_404(Engagement,pk=engagement_id)
    e.delete()
    return HttpResponseRedirect(reverse('event_attendees',kwargs={"event_id": event_id}))

def call_person(request,person_id):
    if request.method == "POST":
        form = CallForm(request.POST)
        if form.is_valid():
            c = Call(**form.cleaned_data)
            c.save()
            print('redirect')
            return HttpResponseRedirect(reverse('calls'))
    else:
        form = CallForm(initial={'receiver':person_id})
    return render(request, "humanity/add_call.html", {"form": form})

def call(request,call_id):
    context = {'call':  get_object_or_404(Call,pk=call_id)}
    return render(request, "humanity/call.html", context)

def edit_call(request,call_id):
    c = get_object_or_404(Call,pk=call_id)
    form = CallForm(instance=c)
    if request.method == "POST":    
        form = CallForm(request.POST,instance=c)
        if form.is_valid():
            update_attrs(c,**form.cleaned_data)
            return HttpResponseRedirect(reverse('calls'))
    else:
        form = CallForm(instance=c)
    return render(request, "humanity/add_call.html", {"form": form})
