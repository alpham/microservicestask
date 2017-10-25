from django.conf.urls import url
from .views import ping_view, search_view


urlpatterns = [
    url(r'^ping/$', ping_view),
    url(r'^search/$', search_view)
]