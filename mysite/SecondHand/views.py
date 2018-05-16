from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from .forms import UserForm,GoodsForm
from .models import User,Category,Goods
from datetime import datetime
# from django.contrib.auth import authenticate,login,logout
import pdb
# Create your views here.

# def index(request):
#     return HttpResponse("Hello,world.You're at the SecondHand.")



def index(request):
    username = request.session.get('username','')
    categorys = Category.objects.all()
    goods_list = Goods.objects.all()

    return render_to_response('SecondHand/index.html',{'categorys':categorys,'username':username,'goodses':goods_list})

def register(request):
    registered = False
    password =None
    errors = []
    username = None
    password_first = None
    password_second = None
    email = None
    now = datetime.now()

    if request.method == 'POST':
        userform = UserForm(data=request.POST)
        if userform.is_valid():
            #获取表单信息
            if not userform.cleaned_data['username']or not userform.cleaned_data['password_first'] or not userform.cleaned_data['password_second'] or not userform.cleaned_data['email']:
                errors.append('You have the option not to fill out')
            else:
                username = userform.cleaned_data['username']
                password_first = userform.cleaned_data['password_first']
                password_second = userform.cleaned_data['password_second']
                email = userform.cleaned_data['email']

            if password_first is not None and password_second is not None:
                if password_first == password_second:
                    password = password_second
                else:
                    errors.append('Your password_first is not equal to password_second')

            if username is not None and password is not None and email is not None:
                filterResult = User.objects.filter(username=username)
                if len(filterResult) > 0:
                    errors.append('username already exists')
                else:
                    user = User.objects.create(username=username, password=password, email=email, time=now)
                    request.session['username'] = username
                    user.save()
                    registered = True
    else:
        userform = UserForm()
    return render(request, 'SecondHand/register.html', {'userform': userform, 'registered': registered,'errors':errors,'username':username})


def login(request):
    errors = []
    username = None
    password = None
    if request.method == 'POST':
        if not request.POST.get('username') or not request.POST.get('password'):
            errors.append('Your username or password is empty')
        else:
            username = request.POST.get('username')
            password = request.POST.get('password')

        if username is not None and password is not None:
            db_username = User.objects.filter(username=username)
            print(db_username)
            if db_username: #判断用户输入的username是否存在
                user = User.objects.filter(username=username,password=password)
                if user:
                    request.session['username'] = username
                    return HttpResponseRedirect('/SecondHand')
                    #return render_to_response('SecondHand/index.html')
                else:
                    errors.append('Your password is incorrect')
            else:
                errors.append('There is no username')
    return render_to_response('SecondHand/login.html',{'errors':errors})

def logout(request):
    try:
        del request.session['username']
    finally:
        return HttpResponseRedirect('/SecondHand')

def backstage(request):
    errors = []
    username = request.session.get('username', '')
    try:
        goods = Goods.objects.get(seller=username)
        print(goods)
        if request.method == 'POST':
            if request.POST.get('update') == '修改商品信息':
                if not request.POST.get('name') or not request.POST.get('trade_location') or not request.POST.get('price') or not request.POST.get('seller_phone') or not request.POST.get('seller_qq'):
                    errors.append('你的修改有误，请重新修改。注：商品信息中的商品名称、交易地点、商品价格、出售者电话、出售者QQ不能为空')
                    return render_to_response('SecondHand/backstage.html', {'username': username, 'goods': goods,'errors':errors})
                else:
                    goods.name = request.POST.get('name')
                    goods.description = request.POST.get('description')
                    goods.trade_location = request.POST.get('trade_location')
                    goods.price = request.POST.get('price')
                    goods.seller_phone = request.POST.get('seller_phone')
                    goods.seller_qq = request.POST.get('seller_qq')
                    goods.save()
                    errors.append('修改成功')
                    return render_to_response('SecondHand/backstage.html',{'username': username, 'goods': goods, 'errors': errors})
            elif request.POST.get('delete') == '删除商品':
                goods.delete()
                errors.append('删除成功')

                goods = Goods.objects.get(seller=username) #原计划一个用户存在多个已发布的商品，当一个商品信息发布后再从数据库读剩下的商品信息，
                # 再返回后台展示页面。此地方只有一个商品，删除后数据库中没有值，报错，执行except

                #解决多商品展示问题：
                    #将所有商品从数据库中读出，在html中遍历，在遍历的同时给予if条件 筛选出username所发布的。
                return render_to_response('SecondHand/backstage.html', {'username': username, 'goods': goods})
    except:
        return render_to_response('SecondHand/backstage.html', {'username': username})
    #return HttpResponseRedirect('/SecondHand/backstage.html') #出现404错误 后面不能加.html
    return render_to_response('SecondHand/backstage.html',{'username':username,'goods':goods}) #当使用render_to_response方法跳转页面时，在什么方法里面调用则url最后显示的就是什么方法的名字

def add_goods(request):
    now = datetime.now()
    username = request.session.get('username', '')
    if request.method == 'POST':
        goodsform = GoodsForm(request.POST,request.FILES)
        if goodsform.is_valid():
            goods=Goods()
            goods.name = goodsform.cleaned_data['name']
            goods.description = goodsform.cleaned_data['description']
            goods.trade_location = goodsform.cleaned_data['trade_location']
            goods.price = goodsform.cleaned_data['price']
            goods.category_id = goodsform.cleaned_data['category']
            goods.picture = goodsform.cleaned_data['picture']
            goods.seller = username
            goods.seller_phone = goodsform.cleaned_data['seller_phone']
            goods.seller_qq = goodsform.cleaned_data['seller_qq']
            goods.publish_time = now
            goods.save()
            #print(name,description,trade_location,price,category,picture,seller_phone,seller_qq)
            #return HttpResponse('ok')
            return HttpResponseRedirect('/SecondHand/backstage')
            #return render_to_response('SecondHand/backstage.html', {'username': username})
    else:
        goodsform = GoodsForm
    return render_to_response('SecondHand/add_goods.html', {'username': username,'goodsform':goodsform})

def pur_goods(request,goods_id):
    username = request.session.get('username', '')
    goods = Goods.objects.get(id=goods_id)
    if request.method == "POST":
        goods.delete()
        return HttpResponseRedirect('/SecondHand')
    return render_to_response('SecondHand/pur_goods.html', {'username': username,'goods':goods})
