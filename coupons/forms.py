# coding: utf-8
from django import forms


class CouponApplyForm(forms.Form):
    """
    这是一个只允许填写优惠卷Code的表单
    """
    code = forms.CharField()
