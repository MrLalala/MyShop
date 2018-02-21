# coding: utf-8

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create/$',
        views.order_create,
        name='order_create'),
    url(r'^admin/order/(?P<order_id>\d+)/$', views.admin_order_detail, name='order_detail'),
    url(r'^admin/order/(?P<order_id>\d+)/pdf/$', views.create_pdf, name='create_pdf'),
]