import pytest
from rest_framework import status

from user.models import User


@pytest.fixture
def email():
    return 'test@email.com'


@pytest.fixture
def password():
    return 'uhbovyvuvuyv879'


def test_create_new_user(api_client, email, password):
    response = api_client.post('/auth/users/', data={
        'email': email,
        'password': password
    })

    assert response.status_code == status.HTTP_201_CREATED, response.data
    assert User.objects.get(email=email)


def test_login(api_client, email, password):
    user = User.objects.create_user(email, password)
    user.set_password(password)
    user.save()

    response = api_client.post('/auth/token/login/', data={
        'email': email,
        'password': password
    })

    assert response.status_code == status.HTTP_200_OK, response.data
    assert 'auth_token' in response.data
