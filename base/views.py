from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
# when user is created they will be automatically logged in
from django.contrib.auth import login

from .models import Agenda


class AgendaLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('agenda-list')

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('agenda-list')

    # if form is valid redirect to url provided
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('agenda-list')
        return super(RegisterPage, self).get(*args, **kwargs)


class AgendaList(LoginRequiredMixin, ListView):
    model = Agenda
    context_object_name = 'agenda_list'

    # allows user to get their data only
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['agenda_list'] = context['agenda_list'].filter(user=self.request.user)
        context['count'] = context['agenda_list'].filter(complete=False).count()
        return context

class AgendaDetail(LoginRequiredMixin, DetailView):
    model = Agenda
    context_object_name = 'agenda'
    template_name = 'base/agenda.html'

class AgendaCreate(LoginRequiredMixin, CreateView):
    model = Agenda
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('agenda-list')

    # user can only create their own agenda
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AgendaCreate, self).form_valid(form)

class AgendaUpdate(LoginRequiredMixin, UpdateView):
    model = Agenda
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('agenda-list')


class AgendaDelete(LoginRequiredMixin, DeleteView):
    model = Agenda
    context_object_name = 'agenda'
    success_url = reverse_lazy('agenda-list')