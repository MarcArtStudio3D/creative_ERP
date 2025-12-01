#!/usr/bin/env python3
"""
Test completo de refresh de campo txtSeccion
Simula exactamente lo que sucede en la interfaz de artículos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication, QLineEdit
from core.db import set_current_database, get_session
from modules.articulos.controller import ArticuloController
from modules.articulos.repository import ArticuloRepository

def simulate_field_refresh():
    """Simula el refresh de campo txtSeccion como en la interfaz real"""
    print("🔧 Simulando refresh de campo txtSeccion...")
    
    # Configurar base de datos
    set_current_database('artstudio3d')
    
    # Crear controller y repository
    controller = ArticuloController()
    repository = ArticuloRepository()
    
    # Simular campo txtSeccion
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
        
    txtSeccion = QLineEdit()
    
    def load_form_from_article(article):
        """Simula _load_form_from_article de view.py"""
        print(f"📝 Cargando formulario para artículo {article.codigo}")
        
        # Obtener sección como hace la view real
        seccion_id = article.id_seccion if hasattr(article, 'id_seccion') else None
        seccion_text = ""
        
        if seccion_id:
            seccion_name = controller.get_seccion_name(seccion_id)
            if seccion_name:
                seccion_text = f"S{seccion_id} - {seccion_name}"
            else:
                seccion_text = "Sin sección"
        else:
            seccion_text = "Sin sección"
        
        # Actualizar campo
        txtSeccion.setText(seccion_text)
        print(f"   txtSeccion actualizado a: '{txtSeccion.text()}'")
        return txtSeccion.text()
    
    # Test con artículos específicos por ID
    print("\n=== Test de refresh con diferentes artículos ===")
    
    # Obtener artículos por ID directamente
    art1 = repository.get_by_id(1)  # ART001 (Sección GENERAL)
    if art1:
        # Crear objeto simulado con atributos
        class MockArticle:
            def __init__(self, data):
                for key, value in data.items():
                    setattr(self, key, value)
        
        article1 = MockArticle(art1)
        result1 = load_form_from_article(article1)
        
    # ART002 (Sección ESPECIAL)  
    art2 = repository.get_by_id(2)
    if art2:
        article2 = MockArticle(art2)
        result2 = load_form_from_article(article2)
        
    # ART003 (Sin sección)
    art3 = repository.get_by_id(3)
    if art3:
        article3 = MockArticle(art3)
        result3 = load_form_from_article(article3)
        
    # Volver a ART001
    if art1:
        result4 = load_form_from_article(article1)
    
    # Verificar que los valores son diferentes
    print(f"\n=== Resultados del refresh ===")
    print(f"ART001 → '{result1}'")
    print(f"ART002 → '{result2}'")
    print(f"ART003 → '{result3}'")
    print(f"ART001 (2da vez) → '{result4}'")
    
    if result1 != result2:
        print("✅ Campo txtSeccion se actualiza correctamente entre artículos")
    else:
        print("❌ Campo txtSeccion NO se actualiza")
        
    if result1 == result4:
        print("✅ Campo mantiene consistencia al volver al mismo artículo")
    else:
        print("❌ Campo pierde consistencia")
    
    return result1, result2, result3, result4

if __name__ == "__main__":
    simulate_field_refresh()