# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Order, OrderItem
from django.core.urlresolvers import reverse
import csv
import datetime
from django.http import HttpResponse


def export_to_csv(modeladmin, request, queryset):
    """
    生成CSV文件
    :param modeladmin: ModelAdmin
    :param request: 服务请求
    :param queryset: 查询集
    :return: HttpResponse
    """
    opts = modeladmin.model._meta
    # 指定Response的回复类型
    response = HttpResponse(content='text/csv')
    # 表示还会有附加文件
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(opts.verbose_name)
    # 创建一个CSV写入对象
    writer = csv.writer(response)
    # 读取opts中的多对多以及一对多字段
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # 写入筛选出来的字段名
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        date_row = []
        for field in fields:
            # 获取字段值
            value = getattr(obj, field.name)
            # 如果是日期格式，就将其格式化为字符串（CSV必须是字符串类型的数据）
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            # 将数据添加进列表中
            date_row.append(value)
        # 想CSV中写入新的一行数据
        writer.writerow(date_row)
    # 返回这个回复
    return response


# short_description=管理页面的动作名
export_to_csv.short_description = 'Export to csv'


def order_detail(obj):
    return '<a href={}>View</a>'.format(
        reverse('orders:order_detail', args=[obj.id])
    )


order_detail.allow_tags = True
order_detail.short_description = "细节"


def order_pdf(obj):
    return '<a href={}>PDF</a>'.format(reverse('orders:create_pdf', args=[obj.id]))


order_pdf.allow_tags = True
order_pdf.short_description = 'PDF 账单'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated', order_detail, order_pdf]
    list_filter = ['paid', 'created', 'updated']
    actions = [export_to_csv, ]
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
# Register your models here.
