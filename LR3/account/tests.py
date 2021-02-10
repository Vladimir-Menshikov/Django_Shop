from django.test import TestCase
import pytest
from .models import Profile
from django.contrib.auth.models import User
from django.urls import reverse
from . import urls, views
import logging

logger = logging.getLogger(__name__)
pytestmark = pytest.mark.django_db

class TestAccount:
    @pytest.fixture
    def fixture_model(self):
        user = User.objects.create_user('username','e@mail.ru', '12345678')
        profile = Profile.objects.create(user = user, verified = False)
        return profile

    def test_model(self, fixture_model):
        assert fixture_model.verified == False
        logger.debug("Account model test passed")

    def test_view(self, client):
        url = reverse('register')
        response = client.get(url)
        assert response.status_code == 200

        url = reverse('login')
        response = client.get(url)
        assert response.status_code == 200

        url = reverse('logout')
        response = client.get(url)
        assert response.status_code == 200
        logger.debug("Account view test passed")
