from django.conf.urls import url
from .views import ping_view


urlpatterns = [
    url(r'^ping/$', ping_view)
]