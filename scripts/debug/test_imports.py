#!/usr/bin/env python3
"""
Archivo temporal para probar la aplicación con importaciones correctas
"""

import sys
from pathlib import Path

# Configurar path correctamente
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def test_imports():
    """Probar todas las importaciones necesarias."""
    try:
        from core.company_manager import company_manager
        print("✅ CompanyManager importado correctamente")
        
        # Probar acceso a empresas
        companies = company_manager.get_available_companies()
        print(f"✅ Empresas disponibles: {len(companies)}")
        
        if companies:
            # Seleccionar primera empresa
            first_company = companies[0]
            success = company_manager.select_company(first_company['id'])
            print(f"✅ Empresa seleccionada: {success}")
            
            if success:
                # Probar importación de modelo Cliente con path relativo
                from modules.clientes.models import Cliente
                print("✅ Modelo Cliente importado correctamente")
                
                # Probar acceso a base de datos
                from core.db import get_session
                session = get_session()
                from sqlmodel import select
                clientes = session.exec(select(Cliente).limit(3)).all()
                print(f"✅ Clientes encontrados: {len(clientes)}")
                session.close()
                
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing imports and functionality...")
    success = test_imports()
    
    if success:
        print("\nEverything is working correctly!")
        print("La aplicación principal debería funcionar.")
    else:
        print("\n❌ Hay problemas que resolver.")