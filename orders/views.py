# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreatedForm
from cart.cart import Cart
from .tasks import order_created


def order_create(request):
    """
    创建订单，创建对应的订单子项，清空购物车
    :param request: 连接请求
    :return: None
    """
    # 获取购物车
    cart = Cart(request)
    if request.method == 'POST':
        # 获取订单
        form = OrderCreatedForm(request.POST)
        if form.is_valid():
            # 保存订单
            order = form.save()
            # 对购物车中每一件商品建立订单子项
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            # 清空购物车
            cart.clear()
            # 后台自动发送邮件
            order_created.delay(order.id)
            # 成功返回订单
            return render(request, 'orders/order/created.html', {'order': order})
    else:
        # 返回空表单
        form = OrderCreatedForm()
    # 返回购物车和空表单
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})

# Create your views here.
