# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class PaymentConfig(AppConfig):
    """
    这是一个AppConfig类，这个类主要用于配置这个APP的初始化等
    """
    # 指定APP名
    name = 'payment'
    # 构建一个可读名
    verbose_name = 'Payment'

    # 在app初始化时做的事
    def ready(self):
        # 导入信号
        import payment.signals
