"""guest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from sign import views
from sign import urls as sign_url

app_name = 'guest'
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r"^$", views.index),  # 添加index/路径
    url(r"^index/$", views.index),  # 添加index/路径
    url(r'^accounts/login/$', views.index),  # 添加index/路径
    url(r"^login_action/$", views.login_action),  # 判断登录是否成功
    url(r"^event_manage/$", views.event_manage),  # 进入发布会管理页
    url(r'^event_search/$', views.event_search),  # 发布会搜索
    url(r'^guest_manage/$', views.guest_manage),  # 进入嘉宾管理页
    url(r'^guest_search/$', views.guest_search),  # 嘉宾搜索
    url(r'^sign_index/(?P<event_id>[0-9]+)/$', views.sign_index),  # 跳转到签到页
    url(r'^sign_index_action/(?P<event_id>[0-9]+)/$', views.sign_index_action),  # 签到动作
    url(r'^logout/$', views.logout),  # 退出
    url(r'^api/', include((sign_url, 'sign'), namespace="sign")),  # 接口路径
]
