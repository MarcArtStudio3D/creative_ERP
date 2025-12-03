#!/usr/bin/env python3
"""
Tests for TarifasBaseView._ensure_tarifas_database to make sure it uses the
currently selected company's database instead of a hardcoded value.
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from PySide6.QtWidgets import QApplication

from core.db import set_current_database, get_current_database
from modules.articulos.view_tarifas_base import TarifasBaseView


@pytest.fixture
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


def test_ensure_uses_company_db(monkeypatch, qapp):
    # Start from main
    set_current_database('main')

    # Simulate a selected company with database_name 'company_42'
    monkeypatch.setattr('core.company_manager.get_current_company_context', lambda: {
        'has_company': True,
        'company_id': 42,
        'database_name': 'company_42'
    })

    # Prevent heavy repository/controller initialization: stub controller class
    class _DummyController:
        def __init__(self, *args, **kwargs):
            self.current = None
            self.index_list = []
        def list_all(self):
            return []

    monkeypatch.setattr('modules.articulos.view_tarifas_base.TarifaTipoController', _DummyController)

    # Stub set_current_database in the view module to capture calls
    calls = []
    def fake_set(db_name):
        calls.append(db_name)
    monkeypatch.setattr('modules.articulos.view_tarifas_base.set_current_database', fake_set)

    # Call the helper directly on a bare instance to avoid heavy UI initialization
    v = TarifasBaseView.__new__(TarifasBaseView)
    v._ensure_tarifas_database()
    # We don't expect the test DB to actually be created in the test env
    # but we DO expect set_current_database to have been invoked with the company db name
    assert calls and calls[0] == 'company_42'


def test_ensure_no_change_when_not_main(monkeypatch, qapp):
    # If current DB is already company-specific, we shouldn't change it
    set_current_database('artstudio3d')

    # Even if company context suggests something else, we keep current
    monkeypatch.setattr('core.company_manager.get_current_company_context', lambda: {
        'has_company': True,
        'company_id': 88,
        'database_name': 'company_88'
    })

    # Stub set_current_database to fail loudly if it would attempt to change
    calls = []
    def fake_set(db_name):
        calls.append(db_name)
    monkeypatch.setattr('modules.articulos.view_tarifas_base.set_current_database', fake_set)

    # Create a bare instance and call the helper directly
    v = TarifasBaseView.__new__(TarifasBaseView)
    v._ensure_tarifas_database()
    # No attempt should be made to switch database because current != 'main'
    assert calls == []


def test_ensure_no_company_selected_leaves_main(monkeypatch, qapp):
    set_current_database('main')

    # No company selected
    monkeypatch.setattr('core.company_manager.get_current_company_context', lambda: {
        'has_company': False
    })

    calls = []
    def fake_set(db_name):
        calls.append(db_name)
    monkeypatch.setattr('modules.articulos.view_tarifas_base.set_current_database', fake_set)
    monkeypatch.setattr('modules.articulos.view_tarifas_base.TarifaTipoController', lambda *a, **k: None)

    v = TarifasBaseView.__new__(TarifasBaseView)
    v._ensure_tarifas_database()
    # No company selected -> no attempt to switch away from main
    assert calls == []
