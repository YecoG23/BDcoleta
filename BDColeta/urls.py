from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^peixes/', include('peixes.urls')),

    # Include the Django admin
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
]
urlpatterns += [
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    # url(r'^messages/', include('django_messages.urls')),
]
