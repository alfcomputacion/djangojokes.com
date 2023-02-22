import json
from django.http import JsonResponse
from django.db.models import Q


from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import Joke, JokeVote
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

    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        order_fields, order_key, direction = self.get_order_settings()

        context['order'] = order_key
        context['direction'] = direction

        # get all but the last order key, which is 'default'
        context['order_fields'] = list(order_fields.keys())[:-1]

        return context

    def get_ordering(self):
        order_fields, order_key, direction = self.get_order_settings()

        ordering = order_fields[order_key]

        # if direction is 'desc' or is invalid use descending order
        if direction != 'asc':
            ordering = '-' + ordering

        return ordering

    def get_order_settings(self):
        order_fields = self.get_order_fields()
        default_order_key = order_fields['default_key']
        order_key = self.request.GET.get('order', default_order_key)
        direction = self.request.GET.get('direction', 'desc')

        # If order_key is invalid, use default
        if order_key not in order_fields:
            order_key = default_order_key

        return (order_fields, order_key, direction)

    def get_order_fields(self):
        # Returns a dict mapping friendly names to field names and lookups.
        return {
            'joke': 'question',
            'category': 'category__category',
            'creator': 'user__username',
            'created': 'created',
            'updated': 'updated',
            'default_key': 'updated'
        }


class JokeListView(ListView):
    model = Joke
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        order_fields, order_key, direction = self.get_order_settings()

        context['order'] = order_key
        context['direction'] = direction

        # get all but the last order key, which is 'default'
        context['order_fields'] = list(order_fields.keys())[:-1]

        return context

    def get_ordering(self):
        order_fields, order_key, direction = self.get_order_settings()

        ordering = order_fields[order_key]

        # if direction is 'desc' or is invalid use descending order
        if direction != 'asc':
            ordering = '-' + ordering

        return ordering

    def get_order_settings(self):
        order_fields = self.get_order_fields()
        default_order_key = order_fields['default_key']
        order_key = self.request.GET.get('order', default_order_key)
        direction = self.request.GET.get('direction', 'desc')

        # If order_key is invalid, use default
        if order_key not in order_fields:
            order_key = default_order_key

        return (order_fields, order_key, direction)

    def get_order_fields(self):
        """
        Returns a dict mapping friendly names to field names and lookups
        """
        return {
            'joke': 'question',
            'category': 'category__category',
            'creator': 'user__username',
            'created': 'created',
            'updated': 'updated',
            'default_key': 'updated'
        }

    # def get_queryset(self):
    #     qs = Joke.objects.all()

    #     if 'slug' in self.kwargs:
    #         slug = self.kwargs['slug']
    #         if '/category' in self.request.path_info:
    #             qs = qs.filter(category__slug=slug)
    #         if '/tag' in self.request.path_info:
    #             qs = qs.filter(tag__slug=slug)
    #     elif 'username' in self.kwargs:
    #         username = self.kwargs['username']
    #         qs = qs.filter(user__username=username)

    #     return qs.order_by(ordering)

    def get_queryset(self):
        ordering = self.get_ordering()
        qs = Joke.objects.all()

        if 'q' in self.request.GET:
            q = self.request.GET.get('q')
            qs = qs.filter(
                Q(question__icontains=q) | Q(answer__icontains=q)
            )
        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
            if '/category' in self.request.path_info:
                qs = qs.filter(category__slug=slug)
            if '/tag' in self.request.path_info:
                qs = qs.filter(tags__slug=slug)
        elif 'username' in self.kwargs:
            username = self.kwargs['username']
            qs = qs.filter(user__username=username)

        return qs.order_by(ordering)


class JokeUpdateView(SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Joke
    form_class = JokeForm
    success_message = 'Joke Updated'

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.user


def vote(request, slug):
    user = request.user  # The logged-in user (or AnonymousUser).
    joke = Joke.objects.get(slug=slug)  # The joke instance.
    data = json.loads(request.body)  # Data from the JavaScript.

    # Set simple variables.
    vote = data['vote']  # The user's new vote.
    likes = data['likes']  # The number of likes currently displayed on page.
    dislikes = data['dislikes']  # The number of dislikes currently displayed.

    if user.is_anonymous:  # User not logged in. Can't vote.
        msg = 'Sorry, you have to be logged in to vote.'
    else:  # User is logged in.
        if JokeVote.objects.filter(user=user, joke=joke).exists():
            # User already voted. Get user's past vote:
            joke_vote = JokeVote.objects.get(user=user, joke=joke)

            if joke_vote.vote == vote:  # User's new vote is the same as old vote.
                msg = 'Right. You told us already. Geez.'
            else:  # User changed vote.
                joke_vote.vote = vote  # Update JokeVote instance.
                joke_vote.save()  # Save.

                # Set data to return to the browser.
                if vote == -1:
                    likes -= 1
                    dislikes += 1
                    msg = "Don't like it after all, huh? OK. Noted."
                else:
                    likes += 1
                    dislikes -= 1
                    msg = 'Grown on you, has it? OK. Noted.'
        else:  # First time user is voting on this joke.
            # Create and save new vote.
            joke_vote = JokeVote(user=user, joke=joke, vote=vote)
            joke_vote.save()

            # Set data to return to the browser.
            if vote == -1:
                dislikes += 1
                msg = "Sorry you didn't like the joke."
            else:
                likes += 1
                msg = "Yeah, good one, right?"

    # Create object to return to browser.
    response = {
        'msg': msg,
        'likes': likes,
        'dislikes': dislikes
    }
    return JsonResponse(response)  # Return object as JSON.
