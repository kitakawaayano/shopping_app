from django.urls import path
from .views import shopping, detail, picture_upload, create
from shoppings import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

app_name = "shopping_app"
urlpatterns = [
    path('shop/', shopping, name='shopping'),
    path('detail/<int:pk>', detail, name='detail'),
    path('', RedirectView.as_view(url='/shop/')),
    path('upload/', picture_upload, name='picture_upload'),
    path('create/', create, name='create'),
    
]

