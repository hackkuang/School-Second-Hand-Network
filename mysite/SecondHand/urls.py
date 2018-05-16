from django.conf.urls import url
from .import views

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^register/$',views.register,name='register'),
    url(r'^login/$',views.login,name='login'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^backstage/$',views.backstage,name='backstage'),
    url(r'^add_goods/$',views.add_goods,name='add_goods'),
    url(r'^pur_goods/(?P<goods_id>[\w\-]+)$',views.pur_goods,name='pur_goods'),
    # url(r'^category/$',views.category,name='category'),
]