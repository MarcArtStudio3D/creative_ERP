import types
from types import SimpleNamespace

from modules.empresas.controller import EmpresasController


def test_crear_y_inicializar_db_calls_set_database(monkeypatch):
    ctrl = EmpresasController()

    # Create a fake empresa object
    empresa = SimpleNamespace(
        id=42,
        host_mariadb='127.0.0.1',
        puerto_mariadb=3306,
        nombre_base_datos_maria_db='company_42_db',
        usuario_mariadb='admin',
        password_mariadb='admin123',
        host_postgresql='127.0.0.1',
        puerto_postgresql=5432,
        nombre_base_datos_postgresql='company_42_pg',
        usuario_postgresql='postgres',
        password_postgresql='postgres'
    )

    # Stub repo.obtener_por_id to return our fake empresa
    monkeypatch.setattr(ctrl.repo, 'obtener_por_id', lambda _id: empresa)

    called = {}

    def fake_set_database_for_company(company_id, init=False, initiator=None):
        called['company_id'] = company_id
        called['init'] = init
        called['initiator'] = initiator

    monkeypatch.setattr('modules.empresas.controller.set_database_for_company', fake_set_database_for_company)

    # Run creation for mariadb
    ok = ctrl.crear_y_inicializar_db(empresa.id, 'mariadb', initiator='testuser')
    assert ok is True
    assert called['company_id'] == empresa.id
    assert called['init'] is True
    assert called['initiator'] == 'testuser'
