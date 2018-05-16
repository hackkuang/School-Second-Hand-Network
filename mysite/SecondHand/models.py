from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=50)
    email = models.EmailField()
    time = models.DateField()

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.name

class Goods(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512,blank=True)  #商品描述
    trade_location = models.CharField(max_length=32)  #交易地点
    price = models.FloatField(default=0)
    category = models.ForeignKey(Category)  #商品种类
    picture = models.ImageField(upload_to='goods',blank=False,null=False)
    seller = models.CharField(max_length=50)
    seller_phone = models.IntegerField(blank=False,null=False)
    seller_qq = models.IntegerField(blank=False,null=False)
    publish_time = models.DateField()

    def __str__(self):
        return self.name