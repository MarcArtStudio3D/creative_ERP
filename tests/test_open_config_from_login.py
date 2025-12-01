#!/usr/bin/env python3
"""Ensure opening the configuration dialog from the login window doesn't crash."""

import sys
from PySide6.QtWidgets import QApplication

from app.views.login_window_multi import LoginWindowMultiCompany


class DummyAuthManager:
    def __init__(self):
        self._current_session = None


def test_open_config_no_crash(monkeypatch):
    app = QApplication.instance() or QApplication(sys.argv)

    auth = DummyAuthManager()
    window = LoginWindowMultiCompany(auth)

    # monkeypatch ConfigDialog.exec so open_config doesn't block and to detect if called
    class _Called(Exception):
        pass

    def fake_exec(self):
        # if this gets called without crashing, we're good; raise to break out
        raise _Called()

    import app.views.config_dialog as cfg
    monkeypatch.setattr(cfg.ConfigDialog, 'exec', fake_exec)

    try:
        # call open_config which will call ConfigDialog(self) and exec() (monkeypatched)
        window.open_config()
    except _Called:
        # expected: exec was called successfully (no crash)
        assert True
    else:
        # should not silently return without calling exec
        assert False, "ConfigDialog.exec was not called"


if __name__ == '__main__':
    sys.exit(test_open_config_no_crash(None))
