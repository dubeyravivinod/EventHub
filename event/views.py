from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Event

# Create your views here.
class EventListView(ListView):
    model = Event
    template_name = 'event/event_list.html'
    context_object_name = 'events'
    
class EventDetailView(DetailView):
    model = Event
    template_name = 'event/event_detail.html'
    context_object_name = 'event'
    
class EventCreateView(CreateView):
    model = Event
    template_name = 'event/event_form.html'
    fields = ['title', 'description', 'date', 'location', 'status']
    success_url = reverse_lazy('event:event_list')
    
class EventUpdateView(UpdateView):
    model = Event
    template_name = 'event/event_form.html'
    fields = ['title', 'description', 'date', 'location', 'status']
    success_url = reverse_lazy('event:event_list')
    
class EventDeleteView(DeleteView):
    model = Event
    template_name = 'event/event_confirm_delete.html'
    success_url = reverse_lazy('event:event_list')
