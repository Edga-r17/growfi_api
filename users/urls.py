from django.urls import path, include
from users.views import *

urlpatterns = [
    path('', UserCreateView.as_view(), name='UserCreateView'),
    path('auth/', UserProfileView.as_view(), name='UserProfileView'),

]