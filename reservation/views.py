from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Reservation

# Create your views here.
class ReservationListView(ListView):
    model = Reservation
    template_name = 'reservation/reservation_list.html'
    context_object_name = 'reservations'

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_authenticated:
            return qs.filter(user=user)
        return qs

class ReservationDetailView(DetailView):
    model = Reservation
    template_name = 'reservation/reservation_detail.html'
    context_object_name = 'reservation'

class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    template_name = 'reservation/reservation_form.html'
    fields = ['event', 'status']
    success_url = reverse_lazy('reservation:reservation_list')

    def form_valid(self, form):
        # populate attendee info from logged-in user
        user = self.request.user
        full_name = user.get_full_name() or user.username
        form.instance.attendee_name = full_name
        form.instance.attendee_email = user.email
        form.instance.user = user
        return super().form_valid(form)

class ReservationUpdateView(LoginRequiredMixin, UpdateView):
    model = Reservation
    template_name = 'reservation/reservation_form.html'
    fields = ['event', 'attendee_name', 'attendee_email', 'status']
    success_url = reverse_lazy('reservation:reservation_list')

    def get_queryset(self):
        # only allow owners to update
        return super().get_queryset().filter(user=self.request.user)

class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    model = Reservation
    template_name = 'reservation/reservation_confirm_delete.html'
    success_url = reverse_lazy('reservation:reservation_list')

    def get_queryset(self):
        # only allow owners to delete
        return super().get_queryset().filter(user=self.request.user)


