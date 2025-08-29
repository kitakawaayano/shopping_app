from django.urls import path
from .views import shopping, detail, create, update, delete, search, cart, buy
from shoppings import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

app_name = "shopping_app"
urlpatterns = [
    path('shop/', shopping, name='shopping'),
    path('detail/<int:pk>', detail, name='detail'),
    path('', RedirectView.as_view(url='/shop/')),
    path('create/', create, name='create'),
    path('update/<int:pk>', update, name='update'),
    path('delete/<int:pk>', delete, name='delete'),
    path('search/', search, name='search'),
    path('cart/user=<str:user>', cart, name='cart'),
    path('cart/user=<str:user>/goods=<goods_id>', cart, name='cart'),
    path('buy/user=<str:user>', buy, name='buy'),
]

