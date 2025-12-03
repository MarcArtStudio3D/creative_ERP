import inspect
from core import db as core_db


def test__ensure_columns_accepts_engine_param():
    sig = inspect.signature(core_db._ensure_columns)
    assert 'engine' in sig.parameters
    # engine should be optional
    assert sig.parameters['engine'].default is None
