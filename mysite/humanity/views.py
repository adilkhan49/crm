from django.shortcuts import render,get_object_or_404, HttpResponseRedirect,reverse
from django.http import HttpResponse
from django.contrib import messages

from .models import Person, Event, Engagement, EngagementRole, Call
from .services import seed_db
from .forms import PersonForm, EventForm, AttendanceForm, CallForm, EngagementFormInvite, EngagementFormConfirmed, EngagementFormAttended


def index(request):
    context = {
        'num_people': Person.objects.count(),
        'num_events': Event.objects.count()
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
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')

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
    context = {'events':  Event.objects.all()}
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
        'event': get_object_or_404(Event,pk=event_id),}
    return render(request, "humanity/event_attendees.html", context)

def calls(request):
    context = {'calls':  Call.objects.all().order_by('-call_time')}
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
        form = CallForm()
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

