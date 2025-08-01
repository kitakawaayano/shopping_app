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
    def get_context_data(self, **kwargs):
        shop = super().get_context_data(**kwargs)
        shop["shops"] = Shops.objects.all
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
            self.queryset = queryset.filter(account_id=user_id).all()
            # print(self.queryset)
            
        else:
            self.queryset = None
        return self.queryset
        
def get_user_id(user):
        try:
            user = Accounts.objects.get(account_name=user).account_id
            return user
        except Accounts.DoesNotExist:
            return None


shopping = IndexView.as_view()
detail = DetailView.as_view()
create = CreateView.as_view()
update = UpdateView.as_view()
delete = DeleteView.as_view()
cart = CartView.as_view()
