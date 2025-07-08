from django.contrib import admin
from .models import Shops, Goods, Accounts, Orderhistory

# modelsをインポートして管理サイトに登録!
# Register your models here.

admin.site.register(Shops)
admin.site.register(Goods)
admin.site.register(Accounts)
admin.site.register(Orderhistory)
