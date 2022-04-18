from django.urls import reverse

from rest_framework import status
from rest_framework.response import Response

import pytest

from src.apps.accounts.models import UserAccount


@pytest.mark.django_db
def test_registration_api_success(unauthorized_api_client, mocker):
    assert UserAccount.objects.count() == 0
    mocked_response = Response(status=status.HTTP_204_NO_CONTENT)
    mocked_login = mocker.patch("src.apps.accounts.services.login.LoginService.login", return_value=mocked_response)

    data = {
        "email": "jane@example.com",
        "first_name": "jane",
        "last_name": "doe",
        "password": "super-secret-password",
    }  # nosec
    response = unauthorized_api_client.post(reverse("api-v1-accounts:registration"), data)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data is None
    assert UserAccount.objects.count() == 1
    user = UserAccount.objects.get()
    mocked_login.assert_called_once_with(mocker.ANY, user)
