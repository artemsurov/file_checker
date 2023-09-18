import pytest
import rest_framework

from model_bakery import baker
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture()
def api_client(db) -> 'rest_framework.test.APIClient':
    client = APIClient()
    return client


@pytest.fixture()
def customer_client(db) -> 'rest_framework.test.APIClient':
    customer = baker.make('user.user')
    token = Token.objects.create(user=customer)

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    client.user = customer
    return client
