import pytest

import colander

from pyramid_sms.validators import valid_us_phone_number


def test_valid_us_phone_number():
    assert valid_us_phone_number(None, "+18082303437") is None


def test_valid_us_phone_number_short():
    assert valid_us_phone_number(None, "8082303437") is None


def test_invalid_us_phone_number_foreign():
    with pytest.raises(colander.Invalid):
        assert valid_us_phone_number(None, "+358407439707") is None


def test_invalid_us_phone_number_no_area_code():
    with pytest.raises(colander.Invalid):
        assert valid_us_phone_number(None, "2303437") is None
