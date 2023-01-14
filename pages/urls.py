from django.urls import path
from .views import AboutusView, HomePageView

app_name = 'pages'
urlpatterns = [ 
    path('', HomePageView.as_view(), name='homepage'),
    path('about-us/', AboutusView.as_view(), name='about-us'),
]