# coding: utf-8

from django import forms

PRODUCT_QUALITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddForm(forms.Form):
    """
    展现一个购物车表单。
    """
    # 限定取值范围在1-20之间
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUALITY_CHOICES,
        coerce=int
    )
    # 是否为更新值？？和Cart类中的update相关。后期补充作用。
    update = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )
