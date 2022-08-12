from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

urlpatterns = [

    path('profile/register/',views.registerProfile, name="profile-register"),
    path('video_feed',views.camerafeed, name ="cam-feed"),

    path('test/<str:pk>/',views.test, name='test'),
]