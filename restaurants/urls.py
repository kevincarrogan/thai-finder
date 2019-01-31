from django.conf.urls import include, url

from . import views


urlpatterns = [
    url(r'^random/$', views.RandomRestaurantView.as_view(), name='random'),
    url(r'^top10/$', views.Top10RestaurantView.as_view(), name='top10'),
]
