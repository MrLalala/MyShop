# coding:utf-8
from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon


class Cart(object):
    def __init__(self, request):
        """
        初始化一个购物车对象
        当全局中不存在购物车时，新建一个购物车；
        当全局中已存在购物车时，指向的就是已存在的购物车
        :param request: request请求
        """
        self.session = request.session
        # 这句话是指从session中获取名字为XXX的值
        cart = self.session.get(settings.CART_SESSION_ID)
        self.coupon_id = request.session.get('coupon_id')
        # 如果没有，就将其初始化为一个空字典
        if not cart:
            # 保存一个空的字典在settings中
            # 原理基于Python字典的浅拷贝。
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def save(self):
        """
        保存购物车的更改
        :return: None
        """
        self.session[settings.CART_SESSION_ID] = self.cart
        # 更改session的修改标记
        self.session.modified = True

    def add(self, product, quantity=1, update_quality=False):
        """
        购物车添加商品
        :param product:商品
        :param quantity: 数量
        :param update_quality:是否为更新后的数量，默认为否
        :return: None
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            # 建立一个用于保存商品单价和数量的二级字典
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price),
            }
        if update_quality:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    @property
    def coupon(self):
        """
        获取优惠券对象
        :return: 优惠券对象或者空对象
        """
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_discount(self):
        """
        计算折扣值
        :return: 减免的金额
        """
        if self.coupon:
            return (self.coupon.discount / Decimal('100')) * self.get_total_price()
        return Decimal('0')

    def get_total_price_after_discount(self):
        """
        计算见面后的价格
        :return: 减免后的价格
        """
        return self.get_total_price() - self.get_discount()

    def remove(self, product):
        """
        移除商品
        :param product:商品ID
        :return: None
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        建立生成器来遍历Cart中的products
        :return: None
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            # 为商品添加新的字段product，值为product对象
            self.cart[str(product.id)]['product'] = product
        # 这里的item即为保存商品数据的二级字典
        for item in self.cart.values():
            # 将字符串转换为Decimal类型的数据
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            # 通过yield返回这个product对象。
            yield item

    def __len__(self):
        """
        :return: 购物车内的商品总数量
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        :return: 购物车的价格总和
        """
        return sum(item['quantity'] * Decimal(item['price']) for item in self.cart.values())

    def clear(self):
        """
        清空购物车
        :return: None
        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
