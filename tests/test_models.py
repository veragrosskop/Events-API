import pytest

import models


def test_user_password_hashing_behaves_correctly(base_url):
    _user = models.User()

    _user.set_password("password_test")
    assert _user.password_hash != "password_test"
    assert _user.password_hash is not None


def test_user_check_password():
    _user = models.User()

    _user.set_password("password_test")
    assert _user.check_password("password_test")

    assert not _user.check_password("wrong_password")
    # assert not _user.check_password('')
    # assert not _user.check_password(None)
    # assert not _user.check_password(False)
    # assert not _user.check_password(0)
    # assert not _user.check_password([])
