import types
from datetime import date as _date

import pytest

from core.utils import qdate_to_date

try:
    from PySide6.QtCore import QDate
    HAS_QT = True
except Exception:
    HAS_QT = False


def test_none_input_returns_none():
    assert qdate_to_date(None) is None


@pytest.mark.skipif(not HAS_QT, reason="PySide6 not available")
def test_qt_qdate_to_date():
    qd = QDate(2023, 11, 20)
    res = qdate_to_date(qd)
    assert isinstance(res, _date)
    assert (res.year, res.month, res.day) == (2023, 11, 20) or (res.year == 2023 and res.month == 11 and res.day == 20)


def test_fake_object_with_toPython():
    class Fake:
        def __init__(self):
            pass

        def isValid(self):
            return True

        def toPython(self):
            return _date(2010, 1, 2)

    f = Fake()
    assert qdate_to_date(f) == _date(2010, 1, 2)


def test_toPython_raises_fallback_to_year_month_day():
    class Fake:
        def __init__(self):
            pass

        def isValid(self):
            return True

        def toPython(self):
            raise RuntimeError("boom")

        def year(self):
            return 2001

        def month(self):
            return 2

        def day(self):
            return 3

    f = Fake()
    assert qdate_to_date(f) == _date(2001, 2, 3)


def test_invalid_qdate_returns_none():
    class Fake:
        def isValid(self):
            return False

    assert qdate_to_date(Fake()) is None


def test_missing_methods_returns_none():
    class Fake:
        pass

    assert qdate_to_date(Fake()) is None
