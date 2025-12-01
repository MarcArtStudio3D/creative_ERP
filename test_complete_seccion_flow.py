#!/usr/bin/env python3
"""
Test completo del flujo de selección y guardado de sección
Simula exactamente lo que hace el usuario en la interfaz
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.db import set_current_database, get_session
from sqlalchemy import text
from modules.articulos.controller import ArticuloController

def test_complete_flow():
    """Test del flujo completo: cargar → seleccionar sección → guardar → verificar"""
    print("🧪 Test completo de flujo de sección")
    print("=" * 60)
    
    # Configurar base de datos
    set_current_database('artstudio3d')
    controller = ArticuloController()
    session = get_session()
    
    # PASO 1: Cargar artículo (simula abrir el formulario)
    print("\n📖 PASO 1: Cargando artículo ART003...")
    article_result = session.execute(text("SELECT id FROM articulos WHERE codigo = 'ART003'")).fetchone()
    if not article_result:
        print("❌ No se encontró artículo ART003")
        return
    
    article_id = article_result[0]
    controller.load_by_id(article_id)
    
    article = controller.get_current_article()
    initial_seccion = article.get('id_seccion')
    print(f"   Artículo cargado: {article['codigo']}")
    print(f"   Sección inicial: {initial_seccion}")
    print(f"   Nombre sección: {controller.get_seccion_name(initial_seccion) if initial_seccion else 'Sin sección'}")
    
    # PASO 2: Seleccionar nueva sección (simula clic en botBuscarSeccion)
    print("\n🔍 PASO 2: Seleccionando nueva sección...")
    new_seccion_id = 1  # GENERAL
    new_seccion_codigo = "S1"
    new_seccion_nombre = "GENERAL"
    
    success = controller.set_seccion_from_lookup(new_seccion_id, new_seccion_codigo, new_seccion_nombre)
    if not success:
        print("❌ Error al establecer sección")
        return
    
    article_after_lookup = controller.get_current_article()
    print(f"✅ Sección seleccionada: {new_seccion_codigo} - {new_seccion_nombre}")
    print(f"   id_seccion en controller: {article_after_lookup.get('id_seccion')}")
    
    # PASO 3: Preparar datos del formulario (simula _save_form_to_article)
    print("\n📝 PASO 3: Preparando datos del formulario...")
    form_data = {
        "codigo": article['codigo'],
        "descripcion_reducida": article.get('descripcion_reducida', 'Artículo de prueba'),
        "coste": article.get('coste', 0),
    }
    
    # CLAVE: Incluir id_seccion desde current_article
    current = controller.get_current_article()
    if 'id_seccion' in current:
        form_data["id_seccion"] = current['id_seccion']
    
    print(f"   Datos a guardar:")
    print(f"   - codigo: {form_data['codigo']}")
    print(f"   - id_seccion: {form_data.get('id_seccion')}")
    
    # PASO 4: Guardar (simula _on_save_clicked)
    print("\n💾 PASO 4: Guardando artículo...")
    success, message = controller.save(form_data)
    print(f"   {'✅' if success else '❌'} {message}")
    
    if not success:
        return
    
    # PASO 5: Verificar en base de datos
    print("\n🔍 PASO 5: Verificando en base de datos...")
    db_result = session.execute(
        text("SELECT codigo, id_seccion FROM articulos WHERE id = :id"),
        {"id": article_id}
    ).fetchone()
    
    print(f"   Base de datos:")
    print(f"   - codigo: {db_result[0]}")
    print(f"   - id_seccion: {db_result[1]}")
    
    # PASO 6: Recargar formulario (simula _load_form_from_article)
    print("\n🔄 PASO 6: Recargando formulario...")
    # El controller ya recargó en save(), pero simulamos el flujo completo
    controller.load_by_id(article_id)
    reloaded = controller.get_current_article()
    seccion_name = controller.get_seccion_name(reloaded.get('id_seccion'))
    
    print(f"   Datos recargados:")
    print(f"   - codigo: {reloaded['codigo']}")
    print(f"   - id_seccion: {reloaded.get('id_seccion')}")
    print(f"   - nombre_seccion: {seccion_name}")
    
    # VERIFICACIÓN FINAL
    print("\n" + "=" * 60)
    if db_result[1] == new_seccion_id and reloaded.get('id_seccion') == new_seccion_id:
        print("✅ ¡TEST EXITOSO! La sección se guardó y persiste correctamente")
        print(f"   Sección guardada: {new_seccion_codigo} - {seccion_name}")
    else:
        print("❌ TEST FALLIDO")
        print(f"   Esperado: {new_seccion_id}")
        print(f"   En BD: {db_result[1]}")
        print(f"   Recargado: {reloaded.get('id_seccion')}")
    
    session.close()

if __name__ == "__main__":
    test_complete_flow()
