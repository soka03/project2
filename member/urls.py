from django.urls import path, include
from .views import *


urlpatterns = [
    path('info/', info),
    path('post/', postlist),
]
