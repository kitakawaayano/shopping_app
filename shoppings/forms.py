from django import forms
from .models import Goods


class GoodsForm(forms.ModelForm):
    class Meta:
        model = Goods
        fields = ["goods_name", "price", "description", "shops_id", "picture", "number"]
        labels = {
            "goods_name":"商品名",
            "price":"価格",
            "description":"説明",
            "shops_id":"お店",
            "picture":"画像",
            "number":"個数",
        }
