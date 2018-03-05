"""bitmerx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
import bitmerx.views as bitmerx_views
import order.views as order_views
import trade.views as trade_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', bitmerx_views.index, name='index'),
    path('order/', order_views.order, name='order'),
    path('my-orders/', order_views.my_orders, name='my-orders'),
    path('my-trades/', trade_views.my_trades, name='my-trades'),
    path('order-book/', order_views.order_book, name='order-book'),
]
