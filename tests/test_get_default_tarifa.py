#!/usr/bin/env python3
"""
Tests for repository.get_default_tarifa to ensure it reads from main.empresas when company selected
"""
import os
import sys

from sqlalchemy import text

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.db import get_session, set_current_database
from modules.articulos.repository import ArticuloRepository


def test_get_default_tarifa_reads_main_empresas(monkeypatch):
    # Ensure we're working with expected DBs
    set_current_database("main")
    session = get_session()

    # Create or update a temporary Empresa with tarifa_predeterminada='777'
    # Use a sufficiently high non-colliding id
    company_id = 987654

    # Try to clean any existing record for this id
    session.execute(text("DELETE FROM empresas WHERE id = :id"), {"id": company_id})
    session.commit()

    session.execute(
        text(
            "INSERT INTO empresas (id, group_id, codigo_empresa, nombre_fiscal, cif_nif, tarifa_predeterminada, activa) VALUES (:id, :group_id, :codigo, :nombre, :cif, :tarifa, 1)"
        ),
        {
            "id": company_id,
            "group_id": 1,
            "codigo": "C-TEST",
            "nombre": "Empresa Test",
            "cif": "TESTCIF",
            "tarifa": "777",
        },
    )
    session.commit()

    # Monkeypatch company context to pretend this company is selected
    monkeypatch.setattr(
        "core.company_manager.get_current_company_context",
        lambda: {"has_company": True, "company_id": company_id},
    )

    # Switch to artstudio3d (repo will internally switch to main when reading company settings)
    set_current_database("artstudio3d")
    repo = ArticuloRepository()

    tarifa = repo.get_default_tarifa()

    assert int(tarifa) == 777
