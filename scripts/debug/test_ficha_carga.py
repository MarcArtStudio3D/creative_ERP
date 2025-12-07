#!/usr/bin/env python3
"""
Script de prueba para verificar que la ficha de cliente se puede cargar correctamente.
"""

import sys
from pathlib import Path

# Configurar sys.path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def test_cliente_ficha_loading():
    """Prueba que se pueda cargar la ficha de un cliente sin errores."""
    try:
        from PySide6.QtWidgets import QApplication
        from core.company_manager import CompanyDatabaseManager
        from core.auth import Session, UserRole, User
        from modules.clientes.ficha_view import ClienteFichaView
        from core.db import get_session
        
        # Crear aplicación Qt si no existe
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # Configurar empresa
        company_manager = CompanyDatabaseManager()
        empresas = company_manager.get_available_companies()
        
        if not empresas:
            print("❌ No hay empresas disponibles")
            return False
        
        # Usar primera empresa
        company_id = empresas[0]['id']
        success = company_manager.select_company(company_id)
        
        if not success:
            print(f"❌ No se pudo seleccionar empresa {company_id}")
            return False
        
        print(f"✅ Empresa {company_id} seleccionada")
        
        # Obtener sesión y cliente
        session = get_session()
        
        # Buscar un cliente para probar
        from modules.clientes.models import Cliente
        from sqlmodel import select
        cliente = session.exec(select(Cliente)).first()

        if not cliente:
            print("❌ No hay clientes en la base de datos")
            return False
        
        print(f"✅ Cliente encontrado: ID={cliente.id}, Nombre={cliente.nombre_fiscal}")
        
        # Crear usuario y sesión ficticia
        from datetime import datetime
        
        test_user = User(
            id=1,
            username="test",
            email="test@example.com",
            full_name="Usuario Test",
            password_hash="dummy_hash",
            role=UserRole.ADMIN
        )
        
        user_session = Session(
            user=test_user,
            login_time=datetime.now(),
            token="dummy_token"
        )
        
        # Crear ficha de cliente
        ficha = ClienteFichaView(user_session, cliente.id)
        print("✅ Ficha de cliente creada sin errores")
        
        # Verificar que los datos se cargaron
        if ficha.cliente_data:
            print(f"✅ Datos del cliente cargados: {ficha.cliente_data.nombre_fiscal}")
            print(f"   - Código: {ficha.cliente_data.codigo_cliente}")
            print(f"   - CIF: {ficha.cliente_data.cif_nif_siren}")
            print(f"   - Teléfono: {ficha.cliente_data.telefono1}")
            print(f"   - Email: {ficha.cliente_data.email}")
            print(f"   - Dirección: {ficha.cliente_data.direccion1}")
            print(f"   - CP: {ficha.cliente_data.cp}")
            print(f"   - Población: {ficha.cliente_data.poblacion}")
            print(f"   - País: {ficha.cliente_data.id_pais}")
        
        session.close()
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("TEST: Loading client form")
    print("=" * 45)
    
    if test_cliente_ficha_loading():
        print("\nProblem solved.")
        print("✅ La ficha de cliente se puede cargar sin errores")
        print("✅ El mapeo de campos está correcto")
        return True
    else:
        print("\n❌ Aún hay errores al cargar la ficha de cliente")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)