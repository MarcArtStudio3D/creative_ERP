#!/usr/bin/env python3
"""
Script de prueba para verificar que el módulo de artículos carga la tabla correctamente
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from PySide6.QtWidgets import QApplication
from modules.articulos.view import ArticulosView
from core.db import init_artstudio3d_db

def test_articulos_table():
    """Probar que se cargan los artículos en la tabla"""
    app = QApplication(sys.argv)
    
    print("Inicializando base de datos...")
    init_artstudio3d_db()
    
    print("Creando vista de artículos...")
    view = ArticulosView()
    
    # Verificar que el modelo tiene artículos
    model = view.articles_model
    count = model.rowCount()
    print(f"Artículos cargados: {count}")
    
    if count > 0:
        print("\n📦 Primeros artículos:")
        for i in range(min(5, count)):
            article = model.get_article(i)
            if article:
                codigo = article.get('codigo', 'N/A')
                desc = article.get('descripcion_reducida', 'N/A')
                stock = article.get('stock_real', 0)
                print(f"  • {codigo} - {desc} (Stock: {stock})")
    
    # Mostrar la ventana
    view.show()
    print(f"\n✅ Ventana de artículos mostrada con {count} artículos")
    print("Presiona Ctrl+C para salir...")
    
    try:
        app.exec()
    except KeyboardInterrupt:
        print("\n👋 Saliendo...")
        sys.exit(0)

if __name__ == "__main__":
    test_articulos_table()