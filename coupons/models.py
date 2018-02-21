# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):
    """
    优惠卷模型类
    """
    # 优惠券码
    code = models.CharField(max_length=50, unique=True)
    # 有效期
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    # 折扣，通过MinXXX和MaxXXX来指定%范围。
    # 这两个是验证器，当超出指定范围时会跑出ValueErrorException
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    # 可用状态
    active = models.BooleanField()

    def __str__(self):
        return self.code
# Create your models here.
