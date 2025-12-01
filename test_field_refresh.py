#!/usr/bin/env python3
"""
Test para verificar el refresh de campos al cambiar entre artículos
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from core.db import set_current_database, get_session
from modules.articulos.controller import ArticuloController
from sqlalchemy import text

def test_field_refresh():
    """Test de refresh de campos entre artículos"""
    
    # Configurar base de datos
    set_current_database('artstudio3d')
    print("✅ Base de datos configurada a: artstudio3d")
    
    # Crear algunos artículos de prueba con secciones diferentes
    session = get_session()
    
    # Asegurar que tenemos secciones
    result = session.execute(text("SELECT COUNT(*) FROM secciones"))
    if result.scalar() == 0:
        print("Creando secciones de prueba...")
        session.execute(text("INSERT INTO secciones (codigo, seccion) VALUES ('S1', 'GENERAL')"))
        session.execute(text("INSERT INTO secciones (codigo, seccion) VALUES ('S2', 'PREMIUM')"))
        session.commit()
    
    # Crear artículos de prueba
    result = session.execute(text("SELECT COUNT(*) FROM articulos"))
    if result.scalar() < 2:
        print("Creando artículos de prueba...")
        session.execute(text("""
            INSERT INTO articulos (codigo, descripcion, id_seccion) 
            VALUES ('ART001', 'Artículo General', 1)
        """))
        session.execute(text("""
            INSERT INTO articulos (codigo, descripcion, id_seccion) 
            VALUES ('ART002', 'Artículo Premium', 2)
        """))
        session.commit()
    
    # Test con controller
    controller = ArticuloController()
    
    # Cargar primer artículo
    articles = session.execute(text("SELECT id, codigo, id_seccion FROM articulos ORDER BY id LIMIT 2")).fetchall()
    
    if len(articles) >= 2:
        print(f"📖 Cargando artículo 1: {articles[0][1]}")
        controller.load_by_id(articles[0][0])
        article1 = controller.get_current_article()
        seccion1_id = article1.get('id_seccion')
        seccion1_name = controller.get_seccion_name(seccion1_id) if seccion1_id else "Sin sección"
        print(f"   -> Sección: {seccion1_name} (ID: {seccion1_id})")
        
        print(f"📖 Cargando artículo 2: {articles[1][1]}")
        controller.load_by_id(articles[1][0])
        article2 = controller.get_current_article()
        seccion2_id = article2.get('id_seccion')
        seccion2_name = controller.get_seccion_name(seccion2_id) if seccion2_id else "Sin sección"
        print(f"   -> Sección: {seccion2_name} (ID: {seccion2_id})")
        
        if seccion1_id != seccion2_id:
            print("✅ Los artículos tienen secciones diferentes - el campo debe actualizarse")
        else:
            print("⚠️ Los artículos tienen la misma sección")
            
        # Simular navegación
        print("🔄 Simulando navegación entre artículos...")
        controller.load_by_id(articles[0][0])
        print(f"Artículo actual: {controller.get_current_article().get('codigo')} - Sección: {controller.get_seccion_name(controller.get_current_article().get('id_seccion'))}")
        
        controller.load_by_id(articles[1][0])
        print(f"Artículo actual: {controller.get_current_article().get('codigo')} - Sección: {controller.get_seccion_name(controller.get_current_article().get('id_seccion'))}")
    
    session.close()
    print("🧪 Test completado - si ves diferentes secciones, el refresh debería funcionar")

if __name__ == "__main__":
    test_field_refresh()