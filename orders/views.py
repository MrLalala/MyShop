# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from .models import OrderItem
from .forms import OrderCreatedForm
from cart.cart import Cart
from .models import Order
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})


@staff_member_required()
def create_pdf(request, order_id):
    from django.http import HttpResponse
    from django.template.loader import render_to_string
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content='application/pdf')
    response['Content-Disposition'] = 'filename=order_{}'.format(order.id)
    # weasyprint.HTML(string=html).write_pdf(
    #     response, stylesheets=[
    #         weasyprint.CSS(
    #             settings.STATIC_ROOT + 'css/pdf.css'
    #         )
    #     ]
    # )
    return response


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
            request.session['order_id'] = order.id
            # 成功返回订单
            # return render(request, 'orders/order/created.html', {'order': order})
            return redirect(reverse('payment:process'))
    else:
        # 返回空表单
        form = OrderCreatedForm()
    # 返回购物车和空表单
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})

# Create your views here.
