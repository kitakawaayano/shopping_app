from django.urls import path
from .views import shopping, detail, create, update, delete, search, cart, delcart, buy, history
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
    # ↓goods_idと対応した商品をカートから削除する
    path('cart/user=<str:user>/goods=<goods_id>', delcart, name='delcart'),
    path('buy/user=<str:user>', buy, name='buy'),
    path('history/user=<str:user>', history, name='history')
]

