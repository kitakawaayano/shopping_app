from django.shortcuts import render, redirect
from django.views import generic, View
from .models import Shops, Goods, Accounts, Orderhistory
from .forms import GoodsForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

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
    
    
class PictureUploadView(View):
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
    
class CreateView(generic.CreateView):
    model = Goods
    template_name = 'shopping/add.html'
    fields = ['goods_name', 'price', 'description', 'shops_id', '']

shopping = IndexView.as_view()
detail = DetailView.as_view()
picture_upload = PictureUploadView.as_view()
create = CreateView.as_view()

