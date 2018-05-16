from django import forms
from .models import Goods

class UserForm(forms.Form):
    username = forms.CharField()
    password_first = forms.CharField(widget=forms.PasswordInput())
    password_second = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()

class GoodsForm(forms.Form):
    name = forms.CharField(max_length=128,help_text="商品名称",widget=forms.TextInput(attrs={'class':'name','placeholder':'最多二十五个字'}))
    description = forms.CharField(max_length=512,help_text='商品详情',widget=forms.Textarea(attrs={'id':'desc','placeholder':'建议填写物品用途、新旧程度、原价等信息'}))
    trade_location=forms.CharField(max_length=32, help_text="交易地点",widget=forms.TextInput(attrs={'id': 'trade_place', 'placeholder': '宿舍、操场、食堂等'}))
    price = forms.IntegerField(help_text="价格", widget=forms.TextInput(attrs={'id': 'price'}))
    category = forms.ChoiceField(choices=[('1', '手机'), ('2', '衣服'),('3','鞋子')])
    picture = forms.FileField()
    seller_phone = forms.IntegerField(widget=forms.TextInput(attrs={'id': 'tel'}))
    seller_qq = forms.IntegerField(widget=forms.TextInput(attrs={'id': 'qq'}))

    # class Meta:
    #     model = Goods
    #     exclude = ('seller','picture_url')