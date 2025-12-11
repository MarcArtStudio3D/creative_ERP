"""
Controller para Divisiones del Almacén (Secciones, Familias, Subfamilias)
Coordina la lógica de negocio entre la vista y el repository.
Arquitectura MVC pura con modelos Dataclass.
"""

from typing import List, Optional, Tuple

from PySide6.QtCore import QCoreApplication

from modules.articulos.divisiones_repository import DivisionesRepository
from modules.articulos.models import Seccion, Familia, Subfamilia


class DivisionesController:
    """Controller para gestionar las divisiones del almacén"""

    def __init__(self):
        self.repository = DivisionesRepository()

        # Estado actual de la navegación (objetos Dataclass)
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
        self.tipo_seleccion = "seccion" if seccion else None

        if seccion:
            return self.repository.obtener_familias_por_seccion(seccion.id)
        return []

    def crear_seccion(self, codigo: str, nombre: str) -> Tuple[bool, str]:
        """Crea una nueva sección directamente"""
        try:
            if not codigo or not nombre:
                return (
                    False,
                    QCoreApplication.translate(
                        "DivisionesController", "Código y nombre son obligatorios"
                    ),
                )

            existente = self.repository.obtener_seccion_por_codigo(codigo)
            if existente:
                return (
                    False,
                    QCoreApplication.translate(
                        "DivisionesController",
                        "Ya existe una sección con el código '{codigo}'",
                    ).format(codigo=codigo),
                )

            # Crear objeto Seccion
            nueva_seccion = Seccion(id=None, codigo=codigo, seccion=nombre)
            self.repository.guardar_seccion(nueva_seccion)
            return (True, "")
        except Exception as e:
            return (False, str(e))

    def actualizar_seccion_actual(self, codigo: str, nombre: str) -> Tuple[bool, str]:
        """Actualiza la sección seleccionada"""
        if not self.seccion_actual:
            return (
                False,
                QCoreApplication.translate(
                    "DivisionesController", "No hay sección seleccionada"
                ),
            )

        try:
            # Verificar duplicados si cambia el código
            if self.seccion_actual.codigo != codigo:
                existente = self.repository.obtener_seccion_por_codigo(codigo)
                if existente and existente['id'] != self.seccion_actual.id:
                    return (
                        False,
                        QCoreApplication.translate(
                            "DivisionesController",
                            "Ya existe una sección con el código '{codigo}'",
                        ).format(codigo=codigo),
                    )

            # Actualizar dict
            seccion_data = {
                'id': self.seccion_actual.id,
                'codigo': codigo,
                'seccion': nombre
            }
            self.repository.guardar_seccion(seccion_data)
            # Actualizar el dict actual
            self.seccion_actual.codigo = codigo
            self.seccion_actual.seccion = nombre
            return (True, "")
        except Exception as e:
            return (False, str(e))

    def borrar_seccion_actual(self) -> Tuple[bool, str]:
        if not self.seccion_actual:
            return (
                False,
                QCoreApplication.translate(
                    "DivisionesController", "No hay sección seleccionada"
                ),
            )

        try:
            familias = self.repository.obtener_familias_por_seccion(
                self.seccion_actual.id
            )
            if familias:
                return (
                    False,
                    QCoreApplication.translate(
                        "DivisionesController",
                        "La sección tiene {n} familias asociadas",
                    ).format(n=len(familias)),
                )

            self.repository.borrar_seccion(self.seccion_actual.id)
            self.seccion_actual = None
            self.tipo_seleccion = None
            return (True, "")
        except Exception as e:
            return (False, str(e))

    # ==================== FAMILIAS ====================

    def obtener_familias_seccion_actual(self) -> List[Seccion]:
        if not self.seccion_actual:
            return []
        return self.repository.obtener_familias_por_seccion(self.seccion_actual.id)

    def seleccionar_familia(self, familia: Optional[Familia]) -> List[Subfamilia]:
        self.familia_actual = familia
        self.subfamilia_actual = None
        self.tipo_seleccion = "familia" if familia else "seccion"

        if familia:
            return self.repository.obtener_subfamilias_por_familia(familia.id)
        return []

    def crear_familia(self, codigo: str, nombre: str) -> Tuple[bool, str]:
        if not self.seccion_actual:
            return (
                False,
                QCoreApplication.translate(
                    "DivisionesController", "Debe seleccionar una sección"
                ),
            )

        try:
            if not codigo or not nombre:
                return (
                    False,
                    QCoreApplication.translate(
                        "DivisionesController", "Código y nombre son obligatorios"
                    ),
                )

            existente = self.repository.obtener_familia_por_codigo(codigo)
            if existente:
                return (
                    False,
                    QCoreApplication.translate(
                        "DivisionesController",
                        "Ya existe una familia con el código '{codigo}'",
                    ).format(codigo=codigo),
                )

            # Crear dict
            familia_data = {
                'codigo': codigo,
                'familia': nombre,
                'id_seccion': self.seccion_actual.id
            }
            self.repository.guardar_familia(familia_data)
            return (True, "")
        except Exception as e:
            return (False, str(e))

    def actualizar_familia_actual(self, codigo: str, nombre: str) -> Tuple[bool, str]:
        if not self.familia_actual:
            return (
                False,
                QCoreApplication.translate(
                    "DivisionesController", "No hay familia seleccionada"
                ),
            )

        try:
            if self.familia_actual.codigo != codigo:
                existente = self.repository.obtener_familia_por_codigo(codigo)
                if existente and existente['id'] != self.familia_actual.id:
                    return (
                        False,
                        QCoreApplication.translate(
                            "DivisionesController",
                            "Ya existe una familia con el código '{codigo}'",
                        ).format(codigo=codigo),
                    )

            familia_data = {
                'id': self.familia_actual.id,
                'codigo': codigo,
                'familia': nombre,
                'id_seccion': self.familia_actual.id_seccion
            }
            self.repository.guardar_familia(familia_data)
            self.familia_actual.codigo = codigo
            self.familia_actual.familia = nombre
            return (True, "")
        except Exception as e:
            return (False, str(e))

    def borrar_familia_actual(self) -> Tuple[bool, str]:
        if not self.familia_actual:
            return (
                False,
                QCoreApplication.translate(
                    "DivisionesController", "No hay familia seleccionada"
                ),
            )

        try:
            subfamilias = self.repository.obtener_subfamilias_por_familia(
                self.familia_actual.id
            )
            if subfamilias:
                return (
                    False,
                    QCoreApplication.translate(
                        "DivisionesController",
                        "La familia tiene {n} subfamilias asociadas",
                    ).format(n=len(subfamilias)),
                )

            self.repository.borrar_familia(self.familia_actual.id)
            self.familia_actual = None
            self.tipo_seleccion = "seccion"
            return (True, "")
        except Exception as e:
            return (False, str(e))

    # ==================== SUBFAMILIAS ====================

    def obtener_subfamilias_familia_actual(self) -> List[Seccion]:
        if not self.familia_actual:
            return []
        return self.repository.obtener_subfamilias_por_familia(self.familia_actual.id)

    def seleccionar_subfamilia(self, subfamilia: Optional[Subfamilia]):
        self.subfamilia_actual = subfamilia
        self.tipo_seleccion = "subfamilia" if subfamilia else "familia"

    def crear_subfamilia(self, codigo: str, nombre: str) -> Tuple[bool, str]:
        if not self.familia_actual:
            return (
                False,
                QCoreApplication.translate(
                    "DivisionesController", "Debe seleccionar una familia"
                ),
            )

        try:
            if not codigo or not nombre:
                return (
                    False,
                    QCoreApplication.translate(
                        "DivisionesController", "Código y nombre son obligatorios"
                    ),
                )

            existente = self.repository.obtener_subfamilias_por_codigo(codigo)
            if existente:
                return (
                    False,
                    QCoreApplication.translate(
                        "DivisionesController",
                        "Ya existe una subfamilia con el código '{codigo}'",
                    ).format(codigo=codigo),
                )

            subfamilia_data = {
                'codigo': codigo,
                'subfamilia': nombre,
                'id_familia': self.familia_actual.id
            }
            self.repository.guardar_subfamilia(subfamilia_data)
            return (True, "")
        except Exception as e:
            return (False, str(e))

    def actualizar_subfamilia_actual(
        self, codigo: str, nombre: str
    ) -> Tuple[bool, str]:
        if not self.subfamilia_actual:
            return (
                False,
                QCoreApplication.translate(
                    "DivisionesController", "No hay subfamilia seleccionada"
                ),
            )

        try:
            if self.subfamilia_actual.codigo != codigo:
                existente = self.repository.obtener_subfamilias_por_codigo(codigo)
                if existente and existente['id'] != self.subfamilia_actual.id:
                    return (
                        False,
                        QCoreApplication.translate(
                            "DivisionesController",
                            "Ya existe una subfamilia con el código '{codigo}'",
                        ).format(codigo=codigo),
                    )

            subfamilia_data = {
                'id': self.subfamilia_actual.id,
                'codigo': codigo,
                'subfamilia': nombre,
                'id_familia': self.subfamilia_actual.id_familia
            }
            self.repository.guardar_subfamilia(subfamilia_data)
            self.subfamilia_actual.codigo = codigo
            self.subfamilia_actual.subfamilia = nombre
            return (True, "")
        except Exception as e:
            return (False, str(e))

    def borrar_subfamilia_actual(self) -> Tuple[bool, str]:
        if not self.subfamilia_actual:
            return (
                False,
                QCoreApplication.translate(
                    "DivisionesController", "No hay subfamilia seleccionada"
                ),
            )

        try:
            self.repository.borrar_subfamilia(self.subfamilia_actual.id)
            self.subfamilia_actual = None
            self.tipo_seleccion = "familia"
            return (True, "")
        except Exception as e:
            return (False, str(e))
