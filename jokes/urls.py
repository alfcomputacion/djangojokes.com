from django.urls import path
from .views import (
    JokeCreateView, JokeDeleteView, JokeDetailView, JokeListView, JokeUpdateView, vote
)
from django.conf.urls.static import static
from django.conf import settings


app_name = 'jokes'
urlpatterns = [
    path('joke/<slug>/update/', JokeUpdateView.as_view(), name='update'),
    path('joke/<slug>/delete/', JokeDeleteView.as_view(), name='delete'),
    path('joke/', JokeCreateView.as_view(), name='create'),
    path('joke/<slug>/', JokeDetailView.as_view(), name='detail'),
    path('joke/<slug>/vote/', vote, name='ajax-vote'),
    path('', JokeListView.as_view(), name='list'),

    path('category/<slug>/', JokeListView.as_view(), name='category'),
    path('tag/<slug>/', JokeListView.as_view(), name='tag'),
    path('creator/<username>/', JokeListView.as_view(), name='creator'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
