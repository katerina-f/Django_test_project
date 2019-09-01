from django.urls import path
from .views import *


urlpatterns = [
    path('categories/', CategoriesData.as_view()),
    path('categories/<str:id>', CategoriesData.as_view()),
]
