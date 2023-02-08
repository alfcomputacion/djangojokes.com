from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import Joke
from .forms import JokeForm
# Create your views here.


class JokeCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Joke
    form_class = JokeForm
    success_message = 'Joke Created'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class JokeDeleteView(UserPassesTestMixin, DeleteView):
    model = Joke
    success_url = reverse_lazy('jokes:list')

    # def delete(self, request, *args, **kwargs):
    #     result = super().delete(request, *args, **kwargs)
    #     messages.success(self.request, 'Joke deleted.')
    #     return result

    def form_valid(self, form):
        messages.success(self.request, 'Joke Deleted.')
        return super().form_valid(form)

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.user


class JokeDetailView(DetailView):
    model = Joke


class JokeListView(ListView):
    model = Joke


class JokeUpdateView(SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Joke
    form_class = JokeForm
    success_message = 'Joke Updated'

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.user
