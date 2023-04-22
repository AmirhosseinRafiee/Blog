from django.urls import path
from website import views

app_name = 'website'

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('newsletter', views.newsletter, name='newsletter'),

]