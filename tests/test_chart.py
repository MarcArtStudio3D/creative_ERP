#!/usr/bin/env python3
"""
Test script para probar el gráfico de barras en el módulo de artículos
"""

import sys
from PySide6.QtWidgets import QApplication
from modules.articulos.view import ArticulosView

def test_chart():
    """Probar la ventana de artículos con gráfico"""
    app = QApplication.instance() or QApplication(sys.argv)
    
    # Crear y mostrar la ventana
    window = ArticulosView()
    window.show()
    
    # Cambiar a la pestaña de gráfica
    window.ui.Pestanas.setCurrentIndex(2)  # Tab de gráfica
    
    # Simular la carga de un artículo para probar el gráfico
    sample_article = {
        'id': 1,
        'codigo': 'ART001',
        'descripcion_reducida': 'Gráfica de Prueba',
        'coste': 50.0,
        'margen': 30.0,
        'stock_real': 25.0
    }
    
    # Simular que el controller devuelve este artículo
    window.controller._current_article = sample_article
    
    # Actualizar el gráfico
    window._update_chart()
    
    print("✅ Ventana de artículos abierta con gráfico activo")
    print("   - Pestaña 'Estadística/Gráfica' seleccionada")
    print("   - Gráfico de barras con datos de prueba")
    print("   - Controles para cambiar entre unidades e importes")
    
    return app.exec()

if __name__ == "__main__":
    try:
        sys.exit(test_chart())
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)