#!/usr/bin/env python3
"""
Script para simular doble clic y ver debug.
"""

import sys
from pathlib import Path

# Configurar sys.path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def simulate_double_click():
    """Simula el doble clic en la tabla de clientes."""
    try:
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import Qt
        from core.company_manager import CompanyDatabaseManager
        from core.db import get_session
        from modules.clientes.view_full import ClientesViewFull
        
        # Crear aplicación Qt si no existe
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        print("Configuring company...")
        
        # Configurar empresa
        company_manager = CompanyDatabaseManager()
        empresas = company_manager.get_available_companies()
        
        company_id = empresas[0]['id']
        success = company_manager.select_company(company_id)
        
        if not success:
            return False
        
        print(f"✅ Empresa {company_id} seleccionada")
        
        # Crear ClientesViewFull
        session = get_session()
        view_full = ClientesViewFull(session=session)
        
        print("Simulating double click...")
        
        # Obtener tabla
        tabla = getattr(view_full.ui, 'tabla_busquedas', None)
        if not tabla:
            print("❌ No se encontró tabla")
            return False
        
        # Obtener modelo
        model = tabla.model()
        if not model or model.rowCount() == 0:
            print("❌ No hay datos en la tabla")
            return False
        
        print(f"✅ Tabla con {model.rowCount()} filas encontrada")
        
        # Simular selección de la primera fila
        selection_model = tabla.selectionModel()
        first_index = model.index(0, 0)
        selection_model.select(first_index, selection_model.SelectionFlag.Select)
        selection_model.setCurrentIndex(first_index, selection_model.SelectionFlag.Current)
        
        print("✅ Primera fila seleccionada")
        
        # Llamar directamente al método abrir_ficha_cliente
        print("Calling abrir_ficha_cliente()...")
        view_full.abrir_ficha_cliente()
        
        print("✅ Método ejecutado")
        
        # Verificar el estado del StackedWidget
        current_page = view_full.ui.stackedWidget.currentIndex()
        print(f"Current page of StackedWidget: {current_page}")
        
        session.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("DOUBLE CLICK SIMULATION")
    print("=" * 35)
    
    if simulate_double_click():
        print("\n✅ Simulación completada")
        return True
    else:
        print("\n❌ Error en simulación")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)