from django.forms import ModelForm, Textarea
from .models import Joke


class JokeForm(ModelForm):
    class Meta:
        model = Joke

        fields = [
            'user', 'category', 'tags', 'question', 'answer'
        ]

        widgets = {
            'question': Textarea(
                attrs={'cols': 80, 'rows': 3, 'autofocus': True}
            ),
            'answer': Textarea(
                attrs={'cols': 80, 'rows': 2, 'placeholder': 'Make it funy!'}
            )
        }
        help_texts = {
            'question': 'No dirty Jokes please.',
            'tags': 'Use Ctrl+click to select multiple tags.'
        }
