from django.urls import path
from homes import views

urlpatterns = [
    path('home/', views.house_api),
    path('my_houses/', views.my_houses_api),
    path('add_house/', views.add_house_api),

]