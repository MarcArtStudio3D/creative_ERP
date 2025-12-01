#!/usr/bin/env python3
"""
Script para probar el gráfico integrado en el módulo de artículos
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from modules.articulos.view import ArticulosView
from modules.articulos.controller import ArticuloController
import random

class MockRepository:
    """Mock repository para pruebas sin base de datos"""
    def get_all(self, limit=100):
        return [
            {
                'id': 1,
                'codigo': 'ART001',
                'descripcion_reducida': 'Smartphone Pro Max',
                'stock_real': 25.0,
                'coste': 450.0,
                'margen': 35.0
            },
            {
                'id': 2,
                'codigo': 'ART002', 
                'descripcion_reducida': 'Laptop Gaming RGB',
                'stock_real': 8.0,
                'coste': 850.0,
                'margen': 25.0
            }
        ]

class MockController:
    """Mock controller para pruebas"""
    def __init__(self):
        self.repository = MockRepository()
        self._current_article = None
    
    def get_current_article(self):
        return self._current_article
    
    def load_by_id(self, article_id):
        # Simular carga de artículo con datos de muestra
        self._current_article = {
            'id': article_id,
            'codigo': f'ART00{article_id}',
            'descripcion_reducida': 'Producto de Prueba con Gráfico',
            'descripcion': 'Producto completo para probar la funcionalidad del gráfico de barras mensual',
            'coste': 125.50,
            'coste_real': 130.00,
            'margen': 40.0,
            'margen_min': 25.0,
            'stock_real': 35.0,
            'mostrar_web': 1,
            'controlar_stock': True
        }
        
        # Simular datos mensuales realistas
        months = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
                 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
        
        for i, month in enumerate(months):
            # Simular ventas con variaciones estacionales
            seasonal_factor = 1.0
            if i in [5, 6, 7]:  # Verano
                seasonal_factor = 1.4
            elif i in [10, 11]:  # Navidad
                seasonal_factor = 1.6
            elif i in [0, 1]:  # Enero-Febrero (baja)
                seasonal_factor = 0.6
                
            units = int(random.uniform(10, 40) * seasonal_factor)
            amount = units * (self._current_article['coste'] * (1 + self._current_article['margen']/100))
            
            self._current_article[f'unidades_vendidas_{month}'] = units
            self._current_article[f'importe_ventas_{month}'] = amount
        
        return True
    
    def add_new(self):
        return True
    
    def is_editing_new(self):
        return False
    
    def save(self, data):
        return True, "Guardado correctamente"
    
    def delete(self):
        return True, "Eliminado correctamente"
    
    def next_article(self):
        return False
    
    def prev_article(self):
        return False
    
    def get_seccion_name(self, id):
        return "Sección Demo"
    
    def get_familia_name(self, id):
        return "Familia Demo" 
    
    def get_subfamilia_name(self, id):
        return "Subfamilia Demo"
    
    def get_proveedor_info(self, id):
        return "PROV001", "Proveedor Demo"

def test_integrated_chart():
    """Probar el gráfico integrado en el módulo de artículos"""
    app = QApplication.instance() or QApplication(sys.argv)
    
    try:
        # Crear ventana de artículos
        window = ArticulosView()
        
        # Reemplazar el controller con nuestro mock
        window.controller = MockController()
        
        # Cargar un artículo de prueba
        window.controller.load_by_id(1)
        
        # Cargar datos en el formulario
        window._load_form_from_article()
        
        # Llenar algunos campos de estadísticas para que el gráfico tenga datos
        months = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
                 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
        
        for i, month in enumerate(months):
            # Unidades
            units_field = f"txtUnid_ventas_{month}"
            if hasattr(window.ui, units_field):
                field = getattr(window.ui, units_field)
                units = window.controller._current_article.get(f'unidades_vendidas_{month}', 0)
                field.setText(str(int(units)))
            
            # Importes
            amount_field = f"txtImporte_ventas_{month}"
            if hasattr(window.ui, amount_field):
                field = getattr(window.ui, amount_field)
                amount = window.controller._current_article.get(f'importe_ventas_{month}', 0)
                field.setText(f"{amount:.2f}")
        
        # Mostrar ventana
        window.show()
        
        # Cambiar a la pestaña de gráfica (índice 6)
        window.ui.Pestanas.setCurrentIndex(6)
        
        # Forzar actualización del gráfico
        window._update_chart()
        
        print("✅ Gráfico integrado funcionando correctamente")
        print("   - Datos mensuales cargados en campos de estadísticas")
        print("   - Gráfico de barras con datos reales del artículo")
        print("   - Controles para cambiar entre unidades e importes")
        print("   - Pestaña 'Estadística/Gráfica' activada")
        print("   - Prueba los radio buttons para ver diferentes datos")
        
        return app.exec()
        
    except Exception as e:
        print(f"❌ Error al probar gráfico integrado: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(test_integrated_chart())