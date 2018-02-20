# coding: utf-8
from celery import shared_task
from django.core.mail import send_mail
from .models import Order


@shared_task
def order_created(order_id):
    """
    当提交订单时发送邮件
    :param order_id: 订单编号
    :return: 邮件
    """
    order = Order.objects.get(id=order_id)
    subject = "Order nr. {}".format(order.id)
    message = "Dear {}, \n\nyou order is success, this id is {}.".format(order.first_name, order.id)
    mail_sent = send_mail(subject,
                          message,
                          '1354410847@qq.com',
                          [order.email, ])
    return mail_sent
