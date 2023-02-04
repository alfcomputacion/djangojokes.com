from django.views.generic import TemplateView
from django.contrib import messages
# Create your views here.


class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class AboutusView(TemplateView):
    template_name = 'pages/about_us.html'

    def get(self, request, *args, **kwargs):
        messages.debug(request, 'Debug messages.')
        messages.info(request, 'Info messages.')
        messages.success(request, 'Success messages.')
        messages.warning(request, 'Warning messages.')
        messages.error(request, 'error messages.')
        return super().get(request, args, kwargs)
