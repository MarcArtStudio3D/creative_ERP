#!/usr/bin/env python3
"""
Verify that the application sets a non-null window icon on initialize.
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.app import CreativeERPApp


def test_app_sets_icon():
    app_obj = CreativeERPApp()
    # Do not call run() - just initialize
    ok = app_obj.initialize()
    assert ok
    qapp = app_obj.qapp
    assert qapp is not None
    # windowIcon should not be null (if resource or path exists)
    icon = qapp.windowIcon()
    assert not icon.isNull(), "Application window icon is null"


if __name__ == "__main__":
    test_app_sets_icon()
    print("OK")
