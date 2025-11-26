#!/usr/bin/env python3
"""
Script de prueba para verificar que el guardado de clientes funciona sin errores.
"""

import sys
from pathlib import Path

# Configurar sys.path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def test_cliente_save():
    """Prueba que se pueda guardar un cliente sin errores."""
    try:
        from core.company_manager import CompanyDatabaseManager
        from core.db import get_session
        from modules.clientes.models import Cliente
        from modules.clientes.repository import ClienteRepository
        from datetime import date
        
        print("🧪 PRUEBA DE GUARDADO DE CLIENTE")
        print("=" * 40)
        
        # Configurar empresa
        company_manager = CompanyDatabaseManager()
        empresas = company_manager.get_available_companies()
        
        if not empresas:
            print("❌ No hay empresas disponibles")
            return False
        
        company_id = empresas[0]['id']
        success = company_manager.select_company(company_id)
        
        if not success:
            print(f"❌ No se pudo seleccionar empresa {company_id}")
            return False
        
        print(f"✅ Empresa {company_id} seleccionada")
        
        # Obtener sesión y crear repositorio
        session = get_session()
        repository = ClienteRepository(session)
        
        print("🔍 Verificando tablas disponibles...")
        from sqlalchemy import inspect
        from core.db import get_engine
        
        engine = get_engine()
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        required_tables = ['clientes', 'historial_clientes', 'deudas_clientes']
        missing_tables = [t for t in required_tables if t not in tables]
        
        if missing_tables:
            print(f"❌ Tablas faltantes: {missing_tables}")
            return False
        
        print("✅ Todas las tablas necesarias están presentes")
        
        # Crear un cliente de prueba
        print("🔄 Creando cliente de prueba...")
        cliente_test = Cliente(
            codigo_cliente="TEST_001",
            nombre_fiscal="Cliente de Prueba Test",
            cif_nif_siren="12345678T",
            telefono1="123456789",
            email="test@ejemplo.com",
            direccion1="Calle Test 123",
            cp="12345",
            poblacion="Ciudad Test",
            provincia="Provincia Test",
            id_pais="España",
            fecha_alta=date.today()
        )
        
        # Intentar guardar el cliente
        print("💾 Guardando cliente...")
        try:
            cliente_guardado = repository.crear(cliente_test)
            print(f"✅ Cliente guardado con ID: {cliente_guardado.id}")
            
            # Verificar que se puede recuperar
            cliente_recuperado = repository.obtener_por_id(cliente_guardado.id)
            if cliente_recuperado:
                print(f"✅ Cliente recuperado: {cliente_recuperado.nombre_fiscal}")
            else:
                print("❌ No se pudo recuperar el cliente guardado")
                return False
            
            # Limpiar - eliminar cliente de prueba
            try:
                session.delete(cliente_recuperado)
                session.commit()
                print("✅ Cliente de prueba eliminado")
            except Exception as e:
                print(f"⚠️ No se pudo eliminar cliente de prueba: {e}")
            
        except Exception as e:
            print(f"❌ Error al guardar cliente: {e}")
            # Intentar rollback
            try:
                session.rollback()
                print("✅ Rollback realizado")
            except Exception as rb_error:
                print(f"❌ Error en rollback: {rb_error}")
            return False
        
        finally:
            session.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    if test_cliente_save():
        print("\n🎉 ¡PRUEBA EXITOSA!")
        print("✅ El guardado de clientes funciona correctamente")
        print("✅ Las tablas necesarias están creadas")
        print("✅ El manejo de sesiones es correcto")
        return True
    else:
        print("\n❌ La prueba falló")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)