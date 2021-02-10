from django.test import TestCase
from .models import Order, OrderItem
import pytest
from app.models import Product, Category
import logging

logger = logging.getLogger(__name__)
pytestmark = pytest.mark.django_db

class TestOrder:
    def test_models(self):
        order = Order.objects.create(first_name = 'Name',
                                     last_name = 'Surname',
                                     email = 'e@mail.ru',
                                     address = 'Street',
                                     postal_code = '228322',
                                     city = 'City',
                                     paid = 0,)
        category = Category.objects.create(name = 'category_name')
        product = Product.objects.create(name = 'name',
                                        description = 'description',
                                        price = 100,
                                        stock = 10,
                                        available = 1,
                                        category = category)
        item = OrderItem.objects.create(order = order,
                                    price = 100,
                                    quantity = 2,
                                    product = product)
        assert order.first_name == 'Name'
        assert order.last_name == 'Surname'
        assert order.email == 'e@mail.ru'
        assert order.address == 'Street'
        assert order.postal_code == '228322'
        assert order.city == 'City'
        assert order.paid == False
        assert item.order == order
        assert item.price == 100
        assert item.quantity == 2
        assert item.product == product
        assert order.get_total_cost() == 200
        assert item.get_cost() == 200
        logger.debug("Order test passed")