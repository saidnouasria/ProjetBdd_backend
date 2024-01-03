from django.urls import path
from .views import house_api 

urlpatterns = [
    path('home/', house_api),

]