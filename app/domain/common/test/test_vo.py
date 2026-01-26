from app.domain.common.vo import DateType
import app.domain.common.vo.date_type as date_type_module
from unittest.mock import Mock
import pendulum
import pytest


def test_create_date_type_with_correct_data(monkeypatch):
    convert_to_tm_mock = Mock(return_value=1700001.0)
    monkeypatch.setattr(date_type_module, "normalize_timestamp", convert_to_tm_mock)
    date = pendulum.now()
    dt = DateType(date)

    convert_to_tm_mock.assert_not_called()

    dt_1 = DateType(17000000000)
    convert_to_tm_mock.assert_called_once_with(17000000000, 10)
    assert dt_1.timestamp == 1700001.0


def test_create_with_error():
    with pytest.raises(Exception):
        DateType("kdkdkdk")
        DateType("kdk2333dkdk")


def test_date_compare_method():
    dt_1 = DateType(17000000000)
    dt_2 = DateType(17000000000)
    dt_3 = DateType(17005000001)
    assert dt_1 == dt_2
    assert dt_3 != dt_1
    assert dt_3 != dt_2

    assert dt_3 > dt_1
    assert dt_2 < dt_3
