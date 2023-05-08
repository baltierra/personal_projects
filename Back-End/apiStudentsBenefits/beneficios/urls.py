from django.urls import re_path
from beneficios import views

#from django.conf.urls.static import static
#from django.conf import settings

urlpatterns=[
    re_path(r'^benefits$',views.benefitsApi),
    re_path(r'^personalized_benefits/',views.personalized_benefits),
    re_path(r'^benefits/([0-9]+)$',views.benefitsApi),
]#+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)