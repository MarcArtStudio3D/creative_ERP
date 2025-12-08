import os

from core.db import init_db, set_current_database


def test_init_db_writes_audit_log(tmp_path):
    """Call init_db with an initiator and verify a log line is emitted.

    This test relies on the project's logs directory being writable in the repository.
    """
    # Ensure we use a non-main DB to avoid accidental main modifications
    set_current_database("artstudio3d")

    # Call init_db with an initiator name
    initiator_name = "pytest_user"
    init_db(initiator=initiator_name)

    # Read the log file created by core.db (logs/init_db.log)
    base = os.path.dirname(os.path.dirname(__file__))
    log_path = os.path.join(base, "logs", "init_db.log")

    assert os.path.exists(log_path), "Expected init_db log file to exist"

    with open(log_path, "r", encoding="utf-8") as fh:
        content = fh.read()

    assert initiator_name in content
