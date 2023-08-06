from django.conf import settings
from django.conf.urls import url
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .views import XLSXExportView


urlpatterns = [
    url(r'^$', login_required(generic.TemplateView.as_view(template_name="index.html")), name="accueil" ),
    url(r'^societes/xlsx/$', csrf_exempt(XLSXExportView.as_view()), name='societes-xlsx'),
]