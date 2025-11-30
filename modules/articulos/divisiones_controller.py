"""
Controller para Divisiones del Almacén (Secciones, Familias, Subfamilias)
Coordina la lógica de negocio entre la vista y el repository
"""

from typing import Optional, List, Tuple
from modules.articulos.divisiones_repository import DivisionesRepository
from modules.articulos.models import Seccion, Familia, Subfamilia


class DivisionesController:
    """Controller para gestionar las divisiones del almacén"""
    
    def __init__(self):
        self.repository = DivisionesRepository()
        
        # Estado actual de la navegación
        self.seccion_actual: Optional[Seccion] = None
        self.familia_actual: Optional[Familia] = None
        self.subfamilia_actual: Optional[Subfamilia] = None
        
        # Tipo de entidad seleccionada para edición ('seccion', 'familia', 'subfamilia')
        self.tipo_seleccion: Optional[str] = None
    
    # ==================== SECCIONES ====================
    
    def obtener_todas_secciones(self) -> List[Seccion]:
        return self.repository.obtener_todas_secciones()
    
    def seleccionar_seccion(self, seccion: Optional[Seccion]) -> List[Familia]:
        self.seccion_actual = seccion
        self.familia_actual = None
        self.subfamilia_actual = None
        self.tipo_seleccion = 'seccion' if seccion else None
        
        if seccion:
            return self.repository.obtener_familias_por_seccion(seccion.id)
        return []
    
    def crear_seccion(self, codigo: str, nombre: str) -> Tuple[bool, str]:
        """Crea una nueva sección directamente"""
        try:
            if not codigo or not nombre:
                return (False, "Código y nombre son obligatorios")
            
            existente = self.repository.obtener_seccion_por_codigo(codigo)
            if existente:
                return (False, f"Ya existe una sección con el código '{codigo}'")
            
            seccion = Seccion(codigo=codigo, seccion=nombre)
            self.repository.guardar_seccion(seccion)
            return (True, "")
        except Exception as e:
            return (False, str(e))
    
    def actualizar_seccion_actual(self, codigo: str, nombre: str) -> Tuple[bool, str]:
        """Actualiza la sección seleccionada"""
        if not self.seccion_actual:
            return (False, "No hay sección seleccionada")
        
        try:
            # Verificar duplicados si cambia el código
            if self.seccion_actual.codigo != codigo:
                existente = self.repository.obtener_seccion_por_codigo(codigo)
                if existente:
                    return (False, f"Ya existe una sección con el código '{codigo}'")
            
            self.seccion_actual.codigo = codigo
            self.seccion_actual.seccion = nombre
            self.repository.guardar_seccion(self.seccion_actual)
            return (True, "")
        except Exception as e:
            return (False, str(e))
            
    def borrar_seccion_actual(self) -> Tuple[bool, str]:
        if not self.seccion_actual:
            return (False, "No hay sección seleccionada")
        
        try:
            familias = self.repository.obtener_familias_por_seccion(self.seccion_actual.id)
            if familias:
                return (False, f"La sección tiene {len(familias)} familias asociadas")
            
            self.repository.borrar_seccion(self.seccion_actual)
            self.seccion_actual = None
            self.tipo_seleccion = None
            return (True, "")
        except Exception as e:
            return (False, str(e))

    # ==================== FAMILIAS ====================
    
    def obtener_familias_seccion_actual(self) -> List[Familia]:
        if not self.seccion_actual:
            return []
        return self.repository.obtener_familias_por_seccion(self.seccion_actual.id)
    
    def seleccionar_familia(self, familia: Optional[Familia]) -> List[Subfamilia]:
        self.familia_actual = familia
        self.subfamilia_actual = None
        self.tipo_seleccion = 'familia' if familia else 'seccion'
        
        if familia:
            return self.repository.obtener_subfamilias_por_familia(familia.id)
        return []
    
    def crear_familia(self, codigo: str, nombre: str) -> Tuple[bool, str]:
        if not self.seccion_actual:
            return (False, "Debe seleccionar una sección")
            
        try:
            if not codigo or not nombre:
                return (False, "Código y nombre son obligatorios")
                
            existente = self.repository.obtener_familia_por_codigo(codigo)
            if existente:
                return (False, f"Ya existe una familia con el código '{codigo}'")
                
            familia = Familia(codigo=codigo, familia=nombre, id_seccion=self.seccion_actual.id)
            self.repository.guardar_familia(familia)
            return (True, "")
        except Exception as e:
            return (False, str(e))
            
    def actualizar_familia_actual(self, codigo: str, nombre: str) -> Tuple[bool, str]:
        if not self.familia_actual:
            return (False, "No hay familia seleccionada")
            
        try:
            if self.familia_actual.codigo != codigo:
                existente = self.repository.obtener_familia_por_codigo(codigo)
                if existente:
                    return (False, f"Ya existe una familia con el código '{codigo}'")
            
            self.familia_actual.codigo = codigo
            self.familia_actual.familia = nombre
            self.repository.guardar_familia(self.familia_actual)
            return (True, "")
        except Exception as e:
            return (False, str(e))

    def borrar_familia_actual(self) -> Tuple[bool, str]:
        if not self.familia_actual:
            return (False, "No hay familia seleccionada")
            
        try:
            subfamilias = self.repository.obtener_subfamilias_por_familia(self.familia_actual.id)
            if subfamilias:
                return (False, f"La familia tiene {len(subfamilias)} subfamilias asociadas")
            
            self.repository.borrar_familia(self.familia_actual)
            self.familia_actual = None
            self.tipo_seleccion = 'seccion'
            return (True, "")
        except Exception as e:
            return (False, str(e))

    # ==================== SUBFAMILIAS ====================
    
    def obtener_subfamilias_familia_actual(self) -> List[Subfamilia]:
        if not self.familia_actual:
            return []
        return self.repository.obtener_subfamilias_por_familia(self.familia_actual.id)
    
    def seleccionar_subfamilia(self, subfamilia: Optional[Subfamilia]):
        self.subfamilia_actual = subfamilia
        self.tipo_seleccion = 'subfamilia' if subfamilia else 'familia'
    
    def crear_subfamilia(self, codigo: str, nombre: str) -> Tuple[bool, str]:
        if not self.familia_actual:
            return (False, "Debe seleccionar una familia")
            
        try:
            if not codigo or not nombre:
                return (False, "Código y nombre son obligatorios")
                
            existente = self.repository.obtener_subfamilias_por_codigo(codigo)
            if existente:
                return (False, f"Ya existe una subfamilia con el código '{codigo}'")
                
            subfamilia = Subfamilia(codigo=codigo, subfamilia=nombre, id_familia=self.familia_actual.id)
            self.repository.guardar_subfamilia(subfamilia)
            return (True, "")
        except Exception as e:
            return (False, str(e))
            
    def actualizar_subfamilia_actual(self, codigo: str, nombre: str) -> Tuple[bool, str]:
        if not self.subfamilia_actual:
            return (False, "No hay subfamilia seleccionada")
            
        try:
            if self.subfamilia_actual.codigo != codigo:
                existente = self.repository.obtener_subfamilias_por_codigo(codigo)
                if existente:
                    return (False, f"Ya existe una subfamilia con el código '{codigo}'")
            
            self.subfamilia_actual.codigo = codigo
            self.subfamilia_actual.subfamilia = nombre
            self.repository.guardar_subfamilia(self.subfamilia_actual)
            return (True, "")
        except Exception as e:
            return (False, str(e))

    def borrar_subfamilia_actual(self) -> Tuple[bool, str]:
        if not self.subfamilia_actual:
            return (False, "No hay subfamilia seleccionada")
            
        try:
            self.repository.borrar_subfamilia(self.subfamilia_actual)
            self.subfamilia_actual = None
            self.tipo_seleccion = 'familia'
            return (True, "")
        except Exception as e:
            return (False, str(e))
