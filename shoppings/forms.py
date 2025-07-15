from django import forms
from .models import Goods

class PictureForm(forms.ModelForm):
    class Meta:
        model = Goods
        fields = ["goods_name", "picture"]
 