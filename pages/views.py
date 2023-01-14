from django.views.generic import TemplateView
# Create your views here.

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class AboutusView(TemplateView):
    template_name = 'pages/about_us.html'
