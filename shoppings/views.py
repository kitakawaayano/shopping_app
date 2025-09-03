from django.shortcuts import render, redirect
from django.views import generic, View
from .models import Shops, Goods, Accounts, Orderhistory
from .forms import GoodsForm, SearchForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
# Create your views here.
# class shopping(generic.ListView):
#     model = Shops
#     template_name = 'shopping/index.html'
    
# class goods(generic.ListView):
#     model = Goods
#     template_name = 'shopping/index.html'

class IndexView(generic.ListView):
    model = Goods
    template_name = 'shopping/index.html'
    def get_queryset(self):
        user_name = self.request.GET.get('user') or self.request.user.username
        try:
            account = Accounts.objects.get(account_name=user_name)
            if account.admin == 1:
                return Goods.objects.all()
            else:
                return Goods.objects.filter(number__gte=1)
        except Accounts.DoesNotExist:
            # アカウントがない
            return Goods.objects.filter(number__gte=1)

    def get_context_data(self, **kwargs):
        shop = super().get_context_data(**kwargs)
        shop["shops"] = Shops.objects.all()
        return shop
     

class DetailView(generic.DetailView):
    model = Goods
    template_name = 'shopping/detail.html'
    
    
class CreateView(View):
    template_name = 'shopping/add_goods.html'
    form_class = GoodsForm
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('./../shop/')
        return render(request, self.template_name, {'form': form})
    
    
class UpdateView(generic.UpdateView):
    model = Goods
    form_class = GoodsForm
    template_name = 'shopping/add_goods.html'
    def get_success_url(self):
        return reverse_lazy('shopping_app:shopping')
    
class DeleteView(generic.DeleteView):
    model = Goods
    template_name = 'shopping/delete.html'
    success_url = reverse_lazy('shopping_app:shopping')


def search(request):
    searchform = SearchForm(request.GET)
    if searchform.is_valid():
        data = searchform.cleaned_data['words']
        # print(data)
        goods = Goods.objects.filter(goods_name__icontains=data)
        # print(goods)
        # print(searchform)
        return render(request, 'shopping/result.html', {'Goods':goods, 'searchform':searchform})
    else:
        print(searchform.errors)
        return render(request, 'shopping/result.html', {'Goods':goods, 'searchform':searchform})
    
class CartView(generic.ListView):
    model = Orderhistory
    template_name = 'shopping/cart.html'
    
    def get_queryset(self, **kwargs):
        user = self.kwargs.get("user")
        user_id = get_user_id(user)
        queryset = super().get_queryset(**kwargs)
        if user_id is not None:
            # 現在購入している者だけを持ってくるようにする
            self.queryset = queryset.filter(account_id=user_id, current_true=True).all()
            # print(self.queryset)
        else:
            self.queryset = None
        return self.queryset
    def my_view(request):
        if request.method == 'GET':
            name = request.GET.get('user', '')
            context = {'received_string': name}
            return render(request, 'shopping/cart.html', context)
        elif request.method == 'POST':
            data = request.POST
            print(data)
            
            
    def post(self, request, *args, **kwargs):
        user = self.kwargs.get("user")
        user_id = get_user_id(user)
        goods_id = request.POST.get("goods_id")
        account = Accounts.objects.get(pk=user_id)
        if user_id and goods_id:
            # 既にカートに同じ商品があれば個数を増やす
            try:
                goods = Goods.objects.get(pk=goods_id)
                print(goods)
                order, created = Orderhistory.objects.get_or_create(
                    account_id=account,
                    goods_id=goods,
                    current_true=True,
                    defaults={"goods_number": 1}
                )
                if not created:
                    order.goods_number += 1
                    order.save()
            except Goods.DoesNotExist:
                pass
        return redirect('shopping_app:cart', user)
    
    
# 名前からidとってくる
def get_user_id(user):
        try:
            user = Accounts.objects.get(account_name=user).account_id
            return user
        except Accounts.DoesNotExist:
            return None


class BuyAllView(generic.ListView):
    model = Orderhistory
    template_name = 'shopping/buy.html'
    
    def get_queryset(self, **kwargs):
        user = self.kwargs.get("user")
        user_id = get_user_id(user)
        queryset = super().get_queryset(**kwargs)
        if user_id is not None:
            self.queryset = queryset.filter(account_id=user_id, current_true=True).all()
            # print(self.queryset)
            
        else:
            self.queryset = None
        return self.queryset
    
    def post(self, request, *args, **kwargs):
        user = self.kwargs.get("user")
        user_id = get_user_id(user)
        if user_id is not None:
            cart_items = Orderhistory.objects.filter(account_id=user_id, current_true=True)
            for item in cart_items:
                # 在庫を減らす
                if item.goods_id and item.goods_id.number >= item.goods_number:
                    item.goods_id.number -= item.goods_number
                    item.goods_id.save()
                # 購入済み
                item.current_true = False
                item.save()
        return redirect('shopping_app:shopping')
    
    
class DelCartView(View):
    def post(self, request, *args, **kwargs):
        user = self.kwargs.get("user")
        user_id = get_user_id(user)
        goods_id = self.kwargs.get("goods_id")

        if user_id and goods_id:
            try:
                cart_item = Orderhistory.objects.get(account_id=Accounts.objects.get(pk=user_id), goods_id=Goods.objects.get(goods_name=goods_id), current_true=True)
                cart_item.delete()
            except Orderhistory.DoesNotExist:
                pass
        return redirect('shopping_app:cart', user)
    
    
class HistoryView(generic.ListView):
    model = Orderhistory
    template_name = 'shopping/history.html'
    
    def get_queryset(self, **kwargs):
        user = self.kwargs.get("user")
        user_id = get_user_id(user)
        queryset = super().get_queryset(**kwargs)
        if user_id is not None:
            # 過去に購入しているものを持ってくるようにする
            self.queryset = queryset.filter(account_id=user_id, current_true=False).all()
        else:
            self.queryset = None
        return self.queryset
    
    
shopping = IndexView.as_view()
detail = DetailView.as_view()
create = CreateView.as_view()
update = UpdateView.as_view()
delete = DeleteView.as_view()
cart = CartView.as_view()
delcart = DelCartView.as_view()
buy = BuyAllView.as_view()
history = HistoryView.as_view()
