from django.urls import re_path
from app_sim import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    re_path(r'^weighted_careers$',views.simulationApi),
    re_path(r'^weighted_careers/$',views.simulationApi),
]

