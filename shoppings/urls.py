from django.urls import path
from .views import shopping

app_name = "shopping_app"
urlpatterns = [
    path('', shopping.as_view(), name='shopping'),
]
