#!/usr/bin/env python3
"""
Test para verificar los datos de secciones que recibimos
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from core.db import set_current_database
from modules.articulos.controller import ArticuloController

def debug_secciones_data():
    """Debug de datos de secciones"""
    
    # Configurar base de datos
    set_current_database('artstudio3d')
    print("✅ Base de datos configurada a: artstudio3d")
    
    # Crear controller
    controller = ArticuloController()
    
    # Obtener datos
    secciones_data = controller.get_secciones_data()
    
    print(f"📊 Número de secciones encontradas: {len(secciones_data)}")
    print("📝 Datos de secciones:")
    
    for i, seccion in enumerate(secciones_data):
        print(f"  [{i}] {seccion}")
        print(f"      id: {seccion.get('id')} (tipo: {type(seccion.get('id'))})")
        print(f"      codigo: {seccion.get('codigo')} (tipo: {type(seccion.get('codigo'))})")
        print(f"      seccion: {seccion.get('seccion')} (tipo: {type(seccion.get('seccion'))})")
        print()

if __name__ == "__main__":
    debug_secciones_data()