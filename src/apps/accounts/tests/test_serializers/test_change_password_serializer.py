from django.test import RequestFactory

from rest_framework.exceptions import ValidationError

import pytest

from src.apps.accounts.api.v1.serializers.password import ChangePasswordSerializer
from src.apps.accounts.exceptions import InvalidPasswordError, WrongPasswordError


OLD_PASSWORD = "OLD_PASSWORD"  # nosec
NEW_PASSWORD = "NEW_PASSWORD"  # nosec


@pytest.fixture()
def change_password_serializer_request(user_account):
    user = user_account()
    user.set_password(OLD_PASSWORD)
    user.save(update_fields=("password",))
    request = RequestFactory()
    request.user = user
    return request


@pytest.mark.django_db
def test_validate_old_password_success(change_password_serializer_request, mocker):
    serializer = ChangePasswordSerializer(context={"request": change_password_serializer_request})
    mocked_check_password = mocker.patch.object(serializer.password_service, "check_password")

    result = serializer.validate_old_password(OLD_PASSWORD)

    assert result == OLD_PASSWORD
    mocked_check_password.assert_called_once_with(change_password_serializer_request.user, OLD_PASSWORD)


@pytest.mark.django_db
def test_validate_new_password_success(change_password_serializer_request, mocker):
    serializer = ChangePasswordSerializer(context={"request": change_password_serializer_request})
    mocked_validate_password = mocker.patch.object(serializer.password_service, "validate_password")

    result = serializer.validate_new_password(NEW_PASSWORD)

    assert result == NEW_PASSWORD
    mocked_validate_password.assert_called_once_with(NEW_PASSWORD, user=change_password_serializer_request.user)


@pytest.mark.django_db
def test_validate_old_password_failure(change_password_serializer_request, mocker):
    serializer = ChangePasswordSerializer(context={"request": change_password_serializer_request})
    mocked_check_password = mocker.patch.object(
        serializer.password_service,
        "check_password",
        side_effect=[WrongPasswordError("test_validate_old_password_failure")],
    )

    with pytest.raises(ValidationError) as exc:
        serializer.validate_old_password(OLD_PASSWORD)

    assert "test_validate_old_password_failure" in str(exc.value)
    mocked_check_password.assert_called_once_with(change_password_serializer_request.user, OLD_PASSWORD)


@pytest.mark.django_db
def test_validate_new_password_failure(change_password_serializer_request, mocker):
    serializer = ChangePasswordSerializer(context={"request": change_password_serializer_request})
    mocked_validate_password = mocker.patch.object(
        serializer.password_service,
        "validate_password",
        side_effect=[InvalidPasswordError("test_validate_new_password_failure")],
    )

    with pytest.raises(ValidationError) as exc:
        serializer.validate_new_password(OLD_PASSWORD)

    assert "test_validate_new_password_failure" in str(exc.value)
    mocked_validate_password.assert_called_once_with(OLD_PASSWORD, user=change_password_serializer_request.user)


@pytest.mark.django_db
def test_save(user_account, mocker):
    serializer = ChangePasswordSerializer(
        data={"old_password": OLD_PASSWORD, "new_password": NEW_PASSWORD},
        context={"request": change_password_serializer_request},
    )
    mocker.patch.object(serializer, "validate_old_password", return_value=OLD_PASSWORD)
    mocker.patch.object(serializer, "validate_new_password", return_value=NEW_PASSWORD)
    mocked_change_password = mocker.patch.object(serializer.password_service, "change_password")

    serializer.is_valid()
    serializer.save()

    mocked_change_password.assert_called_once_with(None, NEW_PASSWORD)
