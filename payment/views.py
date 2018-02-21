# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from decimal import Decimal
from django.core.urlresolvers import reverse
from django.conf import settings
from orders.models import Order
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt


def payment_process(request):
    """
    处理支付网关
    :param request: 求情
    :return: 一个render函数
    """
    order_id = request.session['order_id']
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()
    paypal_dict = {
        # 使用的账户
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        # 支付的总价
        'amount': '%.2f' % Decimal(order.get_total_cost()).quantize(Decimal('.01')),
        # 物品名称
        'item_name': 'Order {}'.format(order.id),
        # 将订单id变成字符串
        'invoice': str(order.id),
        # 设置交易货币,USD即为美金
        'currency_code': 'USD',
        # Paypal的一个借口
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        # 从定向支付成功后的跳转链接
        'return_url': 'http://{}{}'.format(host, reverse('payment:done')),
        # 从定向取消支付或者支付失败的跳转链接
        'cancel_return': 'http://{}{}'.format(host, reverse('payment:canceled')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment/process.html', {'order': order, 'form': form})


# 这个装饰器会让Django忽略CSRF验证
@csrf_exempt
def payment_done(request):
    """
    处理支付成功的view
    :param request:
    :return:
    """
    from cart.cart import Cart
    from orders.tasks import order_created
    # 后台自动发送邮件
    order_created.delay(request.session['order_id'])
    return render(request, 'payment/done.html')


@csrf_exempt
def payment_canceled(request):
    """
    处理支付错误或者取消的函数
    :param request:
    :return:
    """
    return render(request, 'payment/canceled.html')
# Create your views here.
