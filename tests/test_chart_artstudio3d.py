#!/usr/bin/env python3
"""
Script de prueba para verificar el gráfico con la base de datos artstudio3d
"""

import os
import sys

sys.path.insert(0, os.path.abspath("."))

from PySide6.QtWidgets import QApplication

from modules.articulos.view import ArticulosView


def test_chart_with_artstudio3d():
    """Test chart with artstudio3d database"""
    QApplication.instance() or QApplication(sys.argv)

    # La base de datos se configurará automáticamente en ArticulosView
    print("✅ Iniciando aplicación de artículos")

    # Crear ventana de artículos
    window = ArticulosView()

    # Cargar datos de prueba
    window._load_articles_data()

    # Cambiar a la pestaña de gráfica
    window.ui.Pestanas.setCurrentIndex(6)  # Tab gráfica

    # Si hay artículos, tomar el primero para mostrar en el gráfico
    if window.articles_model.rowCount() > 0:
        article = window.articles_model.get_article(0)
        if article:
            window.controller._current_article = article
            window._load_form_from_article()
            window._update_chart()
            print(
                f"✅ Artículo cargado: {article.get('descripcion_reducida', 'Sin nombre')}"
            )

    window.show()

    print("📊 Ventana de artículos abierta con gráfico:")
    print("   - Base de datos: artstudio3d")
    print("   - Pestaña de gráfica activa")
    print("   - Datos mensuales simulados")
    print("   - Controles para cambiar unidades/importes")

    # No ejecutar el bucle de eventos; comprobamos que la ventana se ha creado y la pestaña de gráfica está activa
    assert window.isVisible()
    assert window.ui.Pestanas.currentIndex() == 6


if __name__ == "__main__":
    sys.exit(test_chart_with_artstudio3d())
