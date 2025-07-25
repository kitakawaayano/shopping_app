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

class SearchForm(forms.Form):
    words = forms.CharField(
        label='', 
        max_length=50, 
        widget=forms.TextInput(attrs={
            'placeholder':'キーワードを入力', 
        })
    )
    # keyword = forms.CharField(
    #     label="検索",
    #     max_length=100
    # )
    # target = forms.ChoiceField(label="検索対象", choices=(('goods_name', '商品名')))
    
    # class Meta:
    #     fields = ['keyword', 'target']
    # words = forms.CharField(label="検索", max_length=100)

