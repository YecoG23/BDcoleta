from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
# FAVICON CONFIG
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^peixes/', include('peixes.urls')),

    # Include the Django admin
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    #FAVICON
	url(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico')),
]
urlpatterns += [
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r"^messages/", include("pinax.messages.urls", namespace="pinax_messages")),
]
