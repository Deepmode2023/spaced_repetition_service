import pytest
from app.domain.common.utils import seq
from ..repetition import Repetition, RepetitionStatusEnum
from unittest.mock import Mock
import pendulum


@pytest.mark.parametrize(
    "kwargs",
    (
        {"title": None, "user_id": next(seq)},
        {"title": "", "user_id": next(seq)},
        {"title": "skdfksdkf", "user_id": 10203},
    ),
)
def test_repetition_invariant(kwargs):
    with pytest.raises(Exception):
        Repetition(**kwargs)


def test_existing_repetition(monkeypatch):
    import app.domain.entities.repetition as rp

    _now = pendulum.now()
    fake_mock = Mock(return_value=_now)
    fake_formula_mock = Mock(return_value=1020333)

    monkeypatch.setattr(rp.pendulum, "now", fake_mock)
    monkeypatch.setattr(rp, "repetition_formula", fake_formula_mock)
    rep = Repetition(title="Some title", user_id=next(seq))

    assert rep.count_repetition == 0
    assert rep.id is not None

    rep.update_repetition_schedule(RepetitionStatusEnum.SUCCESSFUL)

    assert rep.count_repetition == 1
    assert rep.date_last_repetition == _now.timestamp()
    assert rep.date_repetition == _now.timestamp() + 1020333
