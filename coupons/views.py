# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon
from .forms import CouponApplyForm


@require_POST
def coupon_apply(request):
    """
    应用优惠券，用于判断优惠劵是否可用，
    如果可用就在session中添加coupon的id
    :param request: 请求
    :return: 到Cart的redirect
    """
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            # 针对Django的DateTimeField，允许在筛选时直接针对时间进行
            # 筛选。
            coupon = Coupon.objects.get(code=code,
                                        valid_from__lt=now,
                                        valid_to__gte=now,
                                        active=True)
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
    return redirect('cart:cart_detail')

# Create your views here.
