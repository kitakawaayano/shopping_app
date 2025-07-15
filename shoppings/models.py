from django.db import models

# Create your models here.

class Shops(models.Model):
    shops_id = models.AutoField(primary_key=True)
    shop_name = models.CharField(max_length=100)

class Goods(models.Model):
    goods_id = models.AutoField(primary_key=True)
    goods_name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField(max_length=200, blank=True, null=True)
    shops_id = models.ForeignKey(Shops, on_delete=models.SET_NULL, null=True, blank=True)
    picture = models.ImageField(upload_to='imgs/')
    number = models.IntegerField()
    
    def __str__(self):
        return self.goods_name or f"Goods {self.goods_id}"
    
class Accounts(models.Model):
    account_id = models.AutoField(primary_key=True)
    account_name = models.CharField(max_length=50)
    point = models.IntegerField()
    admin = models.BooleanField(default=False)
    

class Orderhistory(models.Model):
    account_id = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    goods_id = models.ForeignKey(Goods, on_delete=models.SET_NULL, null=True, blank=True)
    goods_number = models.IntegerField()
    current_true = models.BooleanField(default=True)
