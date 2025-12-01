#!/usr/bin/env python3
"""Test that login dialog sets focus to the password field when shown."""

import sys
from PySide6.QtWidgets import QApplication

from app.views.login_window_multi import LoginWindowMultiCompany


class DummyAuthManager:
    def __init__(self):
        self._current_session = None


def test_login_password_focus():
    app = QApplication.instance() or QApplication(sys.argv)

    auth = DummyAuthManager()
    dlg = LoginWindowMultiCompany(auth)
    # Replace the password_input.setFocus method to record that it was called.
    def _mark_focus():
        dlg._focus_was_called = True

    dlg._focus_was_called = False
    dlg.password_input.setFocus = _mark_focus

    dlg.show()

    # Activate and raise the dialog, then process events so the QTimer singleShot
    # in the implementation has a chance to call setFocus.
    dlg.activateWindow()
    dlg.raise_()
    app.processEvents()

    # allow the event loop to run the pending singleShot
    from PySide6.QtTest import QTest
    QTest.qWait(20)

    assert dlg._focus_was_called, "login dialog should request focus on password_input when shown"


if __name__ == '__main__':
    sys.exit(test_login_password_focus())
