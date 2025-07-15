from django.shortcuts import render, redirect
from django.views import generic, View
from .models import Shops, Goods, Accounts, Orderhistory
from .forms import PictureForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

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
     

class DetailView(View):
    template_name = 'shopping/index.html'
    
    def get(self, request, id):
        picture = Goods.objects.get(goods_id = id)
        picture = Shops.objects.get(shops_id = id)
        return render(request, self.template_name, {'picture': picture})
    
    
class PictureUploadView(View):
    template_name = 'shopping/picture.html'
    form_class = PictureForm
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('detail')
        return render(request, self.template_name, {'form': form})
    

shopping = IndexView.as_view()
detail = DetailView.as_view()
picture_upload = PictureUploadView.as_view()
# create = CreateView.as_view()

