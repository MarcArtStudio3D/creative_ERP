import os

import pytest


def test_ensure_not_running_on_main_blocks_by_default():
    # Import the testable helper from core/alembic_utils
    import core.alembic_utils as env

    url = "mysql+pymysql://user:pw@host:3306/creative_erp_main"

    # Ensure env var not set
    os.environ.pop("ALLOW_ALMIGRATE_MAIN", None)

    with pytest.raises(RuntimeError):
        env.ensure_not_running_migrations_on_main(url)


def test_ensure_not_running_on_main_allows_with_flag(monkeypatch):
    import core.alembic_utils as env

    url = "mysql+pymysql://user:pw@host:3306/creative_erp_main"

    monkeypatch.setenv("ALLOW_ALMIGRATE_MAIN", "1")
    # should not raise
    env.ensure_not_running_migrations_on_main(url)
