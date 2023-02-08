from django.urls import path
from .views import (
    JokeCreateView, JokeDeleteView, JokeDetailView, JokeListView, JokeUpdateView
)
from django.conf.urls.static import static
from django.conf import settings
app_name = 'jokes'
urlpatterns = [
    path('joke/<slug>/update/', JokeUpdateView.as_view(), name='update'),
    path('joke/<slug>/delete/', JokeDeleteView.as_view(), name='delete'),
    path('joke/', JokeCreateView.as_view(), name='create'),
    path('', JokeListView.as_view(), name='list'),
    path('joke/<slug>/', JokeDetailView.as_view(), name='detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
