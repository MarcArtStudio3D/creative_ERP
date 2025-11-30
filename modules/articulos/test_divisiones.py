"""
Script de prueba para verificar que las tablas de divisiones se crean correctamente
"""

import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.db import init_db, get_session, set_current_database
from modules.articulos.models import Seccion, Familia, Subfamilia, Articulo


def test_crear_tablas():
    """Prueba la creación de tablas en la base de datos"""
    print("=" * 60)
    print("TEST: Creación de tablas de divisiones")
    print("=" * 60)
    
    try:
        # Cambiar a base de datos de empresa (ajustar según sea necesario)
        # set_current_database('company_1')  # Descomentar para probar con empresa específica
        
        # Inicializar base de datos
        print("\n1. Inicializando base de datos...")
        init_db()
        print("   ✅ Base de datos inicializada")
        
        # Verificar que las tablas existen
        session = get_session()
        
        print("\n2. Verificando tablas...")
        
        # Intentar contar registros en cada tabla
        count_secciones = session.query(Seccion).count()
        print(f"   ✅ Tabla 'secciones' existe ({count_secciones} registros)")
        
        count_familias = session.query(Familia).count()
        print(f"   ✅ Tabla 'familias' existe ({count_familias} registros)")
        
        count_subfamilias = session.query(Subfamilia).count()
        print(f"   ✅ Tabla 'subfamilias' existe ({count_subfamilias} registros)")
        
        count_articulos = session.query(Articulo).count()
        print(f"   ✅ Tabla 'articulos' existe ({count_articulos} registros)")
        
        print("\n3. Probando creación de datos de ejemplo...")
        
        # Crear una sección de ejemplo
        seccion = Seccion(
            codigo="S001",
            nombre="Electrónica",
            descripcion="Productos electrónicos",
            activo=True
        )
        
        # Verificar si ya existe
        seccion_existente = session.query(Seccion).filter_by(codigo="S001").first()
        if seccion_existente:
            print(f"   ℹ️  Sección 'S001' ya existe, usando la existente")
            seccion = seccion_existente
        else:
            session.add(seccion)
            session.commit()
            session.refresh(seccion)
            print(f"   ✅ Sección creada: {seccion}")
        
        # Crear una familia de ejemplo
        familia_existente = session.query(Familia).filter_by(codigo="F001").first()
        if familia_existente:
            print(f"   ℹ️  Familia 'F001' ya existe")
        else:
            familia = Familia(
                codigo="F001",
                nombre="Smartphones",
                descripcion="Teléfonos inteligentes",
                id_seccion=seccion.id,
                activo=True
            )
            session.add(familia)
            session.commit()
            session.refresh(familia)
            print(f"   ✅ Familia creada: {familia}")
            
            # Crear una subfamilia de ejemplo
            subfamilia = Subfamilia(
                codigo="SF001",
                nombre="Android",
                descripcion="Smartphones Android",
                id_familia=familia.id,
                activo=True
            )
            session.add(subfamilia)
            session.commit()
            session.refresh(subfamilia)
            print(f"   ✅ Subfamilia creada: {subfamilia}")
        
        print("\n" + "=" * 60)
        print("✅ TODAS LAS PRUEBAS PASARON CORRECTAMENTE")
        print("=" * 60)
        
        session.close()
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    exito = test_crear_tablas()
    sys.exit(0 if exito else 1)
