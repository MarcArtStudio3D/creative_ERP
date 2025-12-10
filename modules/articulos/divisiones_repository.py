"""
Repository para Divisiones del Almacén (Secciones, Familias, Subfamilias)
Sigue el patrón Repository para acceso a datos
Migrado a Peewee.
"""

from typing import List, Optional

from peewee import DoesNotExist

from core.peewee_db import ensure_initialized
from modules.articulos.models import Familia, Seccion, Subfamilia


class DivisionesRepository:
    """Repository para gestionar Secciones, Familias y Subfamilias con Peewee"""

    def __init__(self):
        """
        Inicializa el repository con Peewee (no necesita sesión).
        """
        ensure_initialized()

    # ==================== SECCIONES ====================

    def obtener_todas_secciones(self) -> List[Seccion]:
        """Obtiene todas las secciones ordenadas por código"""
        try:
            return list(Seccion.select().order_by(Seccion.codigo))
        except Exception:
            return []

    def obtener_seccion_por_id(self, id_: int) -> Optional[Seccion]:
        """Obtiene una sección por ID"""
        try:
            return Seccion.get_by_id(id_)
        except DoesNotExist:
            return None

    def obtener_seccion_por_codigo(self, codigo: str) -> Optional[Seccion]:
        """Obtiene una sección por código"""
        try:
            return Seccion.get(Seccion.codigo == codigo)
        except DoesNotExist:
            return None

    def guardar_seccion(self, seccion: Seccion) -> Seccion:
        """Guarda o actualiza una sección"""
        seccion.save()
        return seccion

    def borrar_seccion(self, seccion: Seccion) -> bool:
        """
        Borra una sección y todas sus familias y subfamilias asociadas.

        Returns:
            True si se borró correctamente
        """
        try:
            # Primero borrar todas las familias (y sus subfamilias) de esta sección
            familias = self.obtener_familias_por_seccion(seccion.id)
            for familia in familias:
                self.borrar_familia(familia)

            # Luego borrar la sección
            self._session.delete(seccion)
            self._session.commit()
            return True
        except Exception as e:
            self._session.rollback()
            raise e

    def generar_codigo_seccion(self) -> str:
        """Genera el siguiente código de sección disponible (S001, S002, etc.)"""
        ultima = self._session.exec(
            select(Seccion).order_by(Seccion.codigo.desc())
        ).first()
        if not ultima or not ultima.codigo:
            return "S001"

        try:
            # Extrae el número del código (ej: S001 -> 1)
            num = int(ultima.codigo[1:])
            return f"S{num + 1:03d}"
        except (ValueError, IndexError, TypeError):
            # Si el formato es diferente, empezar desde S001
            return "S001"

    # ==================== FAMILIAS ====================

    def obtener_todas_familias(self) -> List[Familia]:
        """Obtiene todas las familias ordenadas por código"""
        stmt = select(Familia).order_by(Familia.codigo)
        return self._session.exec(stmt).all()

    def obtener_familias_por_seccion(self, id_seccion: int) -> List[Familia]:
        """Obtiene todas las familias de una sección específica"""
        stmt = (
            select(Familia)
            .where(Familia.id_seccion == id_seccion)
            .order_by(Familia.codigo)
        )
        return self._session.exec(stmt).all()

    def obtener_familia_por_id(self, id_: int) -> Optional[Familia]:
        """Obtiene una familia por ID"""
        return self._session.get(Familia, id_)

    def obtener_familia_por_codigo(self, codigo: str) -> Optional[Familia]:
        """Obtiene una familia por código"""
        stmt = select(Familia).where(Familia.codigo == codigo)
        return self._session.exec(stmt).first()

    def guardar_familia(self, familia: Familia) -> Familia:
        """Guarda o actualiza una familia"""
        if familia.id is None:
            self._session.add(familia)
        self._session.commit()
        self._session.refresh(familia)
        return familia

    def borrar_familia(self, familia: Familia) -> bool:
        """
        Borra una familia y todas sus subfamilias asociadas.

        Returns:
            True si se borró correctamente
        """
        try:
            # Primero borrar todas las subfamilias de esta familia
            subfamilias = self.obtener_subfamilias_por_familia(familia.id)
            for subfamilia in subfamilias:
                self.borrar_subfamilia(subfamilia)

            # Luego borrar la familia
            self._session.delete(familia)
            self._session.commit()
            return True
        except Exception as e:
            self._session.rollback()
            raise e

    def generar_codigo_familia(self, id_seccion: int) -> str:
        """
        Genera el siguiente código de familia disponible para una sección.
        Formato: F001, F002, etc.
        """
        ultima = self._session.exec(
            select(Familia)
            .where(Familia.id_seccion == id_seccion)
            .order_by(Familia.codigo.desc())
        ).first()

        if not ultima or not ultima.codigo:
            return "F001"

        try:
            # Extrae el número del código (ej: F001 -> 1)
            num = int(ultima.codigo[1:])
            return f"F{num + 1:03d}"
        except (ValueError, IndexError, TypeError):
            # Si el formato es diferente, empezar desde F001
            return "F001"

    # ==================== SUBFAMILIAS ====================

    def obtener_todas_subfamilias(self) -> List[Subfamilia]:
        """Obtiene todas las subfamilias ordenadas por código"""
        stmt = select(Subfamilia).order_by(Subfamilia.codigo)
        return self._session.exec(stmt).all()

    def obtener_subfamilias_por_familia(self, id_familia: int) -> List[Subfamilia]:
        """Obtiene todas las subfamilias de una familia específica"""
        stmt = (
            select(Subfamilia)
            .where(Subfamilia.id_familia == id_familia)
            .order_by(Subfamilia.codigo)
        )
        return self._session.exec(stmt).all()

    def obtener_subfamilias_por_id(self, id_: int) -> Optional[Subfamilia]:
        """Obtiene una subfamilia por ID"""
        return self._session.get(Subfamilia, id_)

    def obtener_subfamilias_por_codigo(self, codigo: str) -> Optional[Subfamilia]:
        """Obtiene una subfamilia por código"""
        stmt = select(Subfamilia).where(Subfamilia.codigo == codigo)
        return self._session.exec(stmt).first()

    def guardar_subfamilia(self, subfamilia: Subfamilia) -> Subfamilia:
        """Guarda o actualiza una subfamilia"""
        if subfamilia.id is None:
            self._session.add(subfamilia)
        self._session.commit()
        self._session.refresh(subfamilia)
        return subfamilia

    def borrar_subfamilia(self, subfamilia: Subfamilia) -> bool:
        """
        Borra una subfamilia.

        Returns:
            True si se borró correctamente
        """
        try:
            self._session.delete(subfamilia)
            self._session.commit()
            return True
        except Exception as e:
            self._session.rollback()
            raise e

    def generar_codigo_subfamilia(self, id_familia: int) -> str:
        """
        Genera el siguiente código de subfamilia disponible para una familia.
        Formato: SF001, SF002, etc.
        """
        ultima = self._session.exec(
            select(Subfamilia)
            .where(Subfamilia.id_familia == id_familia)
            .order_by(Subfamilia.codigo.desc())
        ).first()

        if not ultima or not ultima.codigo:
            return "SF001"

        try:
            # Extrae el número del código (ej: SF001 -> 1)
            num = int(ultima.codigo[2:])
            return f"SF{num + 1:03d}"
        except (ValueError, IndexError, TypeError):
            # Si el formato es diferente, empezar desde SF001
            return "SF001"
