from django.test import TestCase
from .models import Product, Category
import pytest
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)
pytestmark = pytest.mark.django_db

class TestApp:
    def test_models(self):
        category = Category.objects.create(name = 'category_name')
        product = Product.objects.create(name = 'name',
                                        description = 'description',
                                        price = 100,
                                        stock = 10,
                                        available = 1,
                                        category = category)
        assert product.name == 'name'
        assert product.description == 'description'
        assert product.price == 100
        assert product.stock == 10
        assert product.available == True
        assert product.category == category
        assert category.name == 'category_name'
        logger.debug("App test passed")
