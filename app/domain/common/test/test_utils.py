from app.domain.common.utils.arguments import (
    seive_fields,
    process_field,
    validate_mandatory_field,
    SieveValueErrorExceptionExternal,
)
from app.domain.common.models import ClassArgument
import pytest
from unittest.mock import Mock
from app.domain.common.utils.snowflake import (
    seq,
    sequence_mask,
    data_center_id_shift,
    data_center_id_bits,
    snowflake_to_timestamp,
    generator,
)
import time


def test_validate_mandatory_field_with_error():
    with pytest.raises(SieveValueErrorExceptionExternal):
        acc = {}
        validate_mandatory_field("boma", {"boma": None}, acc)


def test_validate_mandatory_field():
    acc = {}
    validate_mandatory_field("boma", {"boma": 2020}, acc)

    assert acc == {"boma": 2020}


def test_process_field():
    acc = {}
    process_field("boma", {"boma": 20303}, acc)
    assert acc == {"boma": 20303}
    process_field("doma", {"boma": 3000}, acc)
    assert acc == {"boma": 20303}
    process_field("doma", {"doma": 3001}, acc)
    assert acc == {"boma": 20303, "doma": 3001}


def test_seive_fields():
    kwargs = seive_fields(
        dogma="dogma",
        zoma=None,
        required_fields=[
            ClassArgument("zoma", True),
            ClassArgument("dogma", False),
        ],
    )

    assert kwargs == {"dogma": "dogma"}


def test_seive_fields_with_error():
    with pytest.raises(TypeError):
        seive_fields(
            dogma="dogma",
            zoma="zomaTV",
            required_fields=[
                123,
                "sldld",
            ],
        )
        seive_fields(
            zoma="zomaTV",
            required_fields=[
                "4",
                "sldld",
            ],
        )


def test_seive_fields_with_unrequired_but_non_empty_value():
    kwargs = seive_fields(
        dogma="dogma",
        zoma="zomaTV",
        required_fields=[
            ClassArgument("zoma", True),
            ClassArgument("dogma", False),
        ],
    )

    assert kwargs == {
        "dogma": "dogma",
        "zoma": "zomaTV",
    }


def test_invariant_seq():
    with pytest.raises(Exception):
        next(seq(-100, -200))


def test_corrected_insert_datacenter_id_in_seq():
    snowflake_id = next(seq)

    datacenter_from_id = (snowflake_id >> data_center_id_shift) & (
        (1 << data_center_id_bits) - 1
    )

    assert 1 == datacenter_from_id


def test_corrected_insert_seq():
    snowflake_id = next(seq)
    sequence_from_id = snowflake_id & sequence_mask
    assert 0 == sequence_from_id

    snowflake_id = next(seq)
    sequence_from_id = snowflake_id & sequence_mask

    assert 1 == sequence_from_id


def test_snowflake_to_timestamp(monkeypatch):
    timestamp = 1700000000000

    mock_time = Mock(return_value=timestamp / 1000)
    monkeypatch.setattr(time, "time", mock_time)

    seq = generator(1, 1)
    snowflake_id = next(seq)

    mock_time.assert_called_once()

    tm = snowflake_to_timestamp(snowflake_id)

    assert tm == timestamp / 1000
