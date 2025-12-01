#!/usr/bin/env python3
"""
Test de guardado de sección en artículos
Verifica que el id_seccion se guarda correctamente en la base de datos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.db import set_current_database, get_session
from sqlalchemy import text
from modules.articulos.controller import ArticuloController
from modules.articulos.repository import ArticuloRepository

def test_save_seccion():
    """Test completo de guardado de sección"""
    print("🧪 Test de guardado de sección en artículos")
    print("=" * 50)
    
    # Configurar base de datos
    set_current_database('artstudio3d')
    
    # Crear controller
    controller = ArticuloController()
    repository = ArticuloRepository()
    
    # Obtener artículo ART001
    session = get_session()
    article_result = session.execute(text("SELECT id FROM articulos WHERE codigo = 'ART001'")).fetchone()
    
    if not article_result:
        print("❌ No se encontró artículo ART001")
        return
    
    article_id = article_result[0]
    print(f"📄 Artículo encontrado: ART001 (ID: {article_id})")
    
    # Cargar artículo en controller
    controller.load_by_id(article_id)
    
    # Verificar estado inicial
    initial_article = controller.get_current_article()
    print(f"📊 Estado inicial - id_seccion: {initial_article.get('id_seccion')}")
    
    # Simular selección de sección (como hace _on_buscar_seccion_clicked)
    print("\n🔍 Simulando selección de sección...")
    seccion_id = 2  # Sección ESPECIAL
    seccion_codigo = "S2"
    seccion_nombre = "ESPECIAL"
    
    success = controller.set_seccion_from_lookup(seccion_id, seccion_codigo, seccion_nombre)
    if not success:
        print("❌ Error al establecer sección en controller")
        return
    
    print(f"✅ Sección establecida en controller: {seccion_codigo} - {seccion_nombre}")
    
    # Verificar que se actualizó en current_article
    updated_article = controller.get_current_article()
    print(f"📊 Estado después de lookup - id_seccion: {updated_article.get('id_seccion')}")
    
    # Simular guardado (como hace _save_form_to_article + controller.save)
    print("\n💾 Simulando guardado...")
    form_data = {
        "codigo": "ART001",
        "descripcion_reducida": "Artículo de prueba",
        "coste": 10.0,
        "id_seccion": updated_article.get('id_seccion')  # Este es el campo clave
    }
    
    print(f"📋 Datos a guardar: id_seccion = {form_data.get('id_seccion')}")
    
    # Guardar
    success, message = controller.save(form_data)
    print(f"{'✅' if success else '❌'} Resultado guardado: {message}")
    
    if not success:
        return
    
    # Verificar en base de datos
    print("\n🔍 Verificando en base de datos...")
    db_result = session.execute(
        text("SELECT id, codigo, id_seccion FROM articulos WHERE id = :id"),
        {"id": article_id}
    ).fetchone()
    
    if db_result:
        print(f"📊 Base de datos - Artículo {db_result[1]}:")
        print(f"   id_seccion = {db_result[2]}")
        
        if db_result[2] == seccion_id:
            print("✅ ¡Sección guardada correctamente!")
        else:
            print(f"❌ ERROR: Sección no coincide (esperado: {seccion_id}, obtenido: {db_result[2]})")
    else:
        print("❌ No se encontró el artículo en la base de datos")
    
    # Recargar y verificar
    print("\n🔄 Recargando artículo para verificar persistencia...")
    controller.load_by_id(article_id)
    reloaded = controller.get_current_article()
    seccion_name = controller.get_seccion_name(reloaded.get('id_seccion'))
    
    print(f"📊 Artículo recargado:")
    print(f"   id_seccion = {reloaded.get('id_seccion')}")
    print(f"   nombre_seccion = {seccion_name}")
    
    if reloaded.get('id_seccion') == seccion_id:
        print("✅ ¡Verificación completa exitosa!")
    else:
        print("❌ La sección no persistió correctamente")
    
    session.close()

if __name__ == "__main__":
    test_save_seccion()
