"""
Controller para el módulo de Artículos usando Peewee.
Sigue el patrón MVC: maneja la lógica de negocio entre la vista y el repository.
"""

import logging
from typing import Any, Dict, List, Optional, Tuple

from PySide6.QtCore import QCoreApplication

from .peewee_repository_clean import ArticuloRepository

logger = logging.getLogger(__name__)


class ArticuloController:
    """Controlador para el módulo de Artículos."""

    def __init__(self):
        """Inicializar controller con Peewee (sin sesión explícita)."""
        self.repository = ArticuloRepository()
        self.current_article = None
        self.is_new = False
        self.codigo_anterior = None

    # ==================== Lifecycle ====================

    def add_new(self) -> bool:
        """Crear un nuevo artículo temporal."""
        try:
            new_id = self.repository.create()
            if not new_id:
                return False

            # Create tarifas for the new article
            self.repository.create_tarifas_for_article(new_id)

            # Load the new article
            self.current_article = self.repository.get_by_id(new_id)
            self.is_new = True
            self.codigo_anterior = self.current_article.get("codigo") if self.current_article else None

            return True
        except Exception as e:
            logger.exception("Error creating article: %s", e)
            return False

    def load_by_id(self, articulo_id: int) -> bool:
        """Cargar un artículo por su ID."""
        try:
            article = self.repository.get_by_id(articulo_id)
            if article:
                self.current_article = article
                self.is_new = False
                self.codigo_anterior = article.get("codigo")
                return True
            return False
        except Exception as e:
            logger.exception("Error loading article: %s", e)
            return False

    def save_current_article(self, form_data: Dict[str, Any] = None) -> Tuple[bool, str]:
        """Guardar el artículo actual."""
        if not self.current_article:
            return False, "No hay artículo cargado"

        try:
            article_id = self.current_article.get("id")
            if not article_id:
                return False, "ID de artículo inválido"

            # Use form_data if provided, otherwise use current_article
            data = form_data if form_data else self.current_article

            # Remove keys that shouldn't be saved
            save_data = {k: v for k, v in data.items() if k != "id"}

            success = self.repository.update(article_id, save_data)

            if success:
                # Reload to get updated data
                self.load_by_id(article_id)
                return True, "Artículo guardado correctamente"
            else:
                return False, "Error al guardar el artículo"

        except Exception as e:
            logger.exception("Error saving article: %s", e)
            return False, f"Error: {str(e)}"

    def delete_article(self, articulo_id: int) -> bool:
        """Eliminar un artículo."""
        try:
            return self.repository.delete(articulo_id)
        except Exception as e:
            logger.exception("Error deleting article: %s", e)
            return False

    def undo_current_article(self):
        """Deshacer cambios en el artículo actual (recargar desde BD)."""
        if self.current_article and self.current_article.get("id"):
            self.load_by_id(self.current_article["id"])

    # ==================== Navigation ====================

    def next_article(self) -> bool:
        """Navegar al siguiente artículo."""
        if not self.current_article:
            return False

        try:
            next_art = self.repository.get_next(self.current_article["id"])
            if next_art:
                self.current_article = next_art
                self.is_new = False
                self.codigo_anterior = next_art.get("codigo")
                return True
            return False
        except Exception as e:
            logger.exception("Error navigating to next article: %s", e)
            return False

    def prev_article(self) -> bool:
        """Navegar al artículo anterior."""
        if not self.current_article:
            return False

        try:
            prev_art = self.repository.get_prev(self.current_article["id"])
            if prev_art:
                self.current_article = prev_art
                self.is_new = False
                self.codigo_anterior = prev_art.get("codigo")
                return True
            return False
        except Exception as e:
            logger.exception("Error navigating to previous article: %s", e)
            return False

    # ==================== Queries ====================

    def get_articles(
        self,
        limit: int = None,
        offset: int = 0,
        order_by: str = "descripcion_reducida",
        order_dir: str = "ASC",
        filtro: str = ""
    ) -> List[Dict]:
        """Obtener lista de artículos."""
        try:
            arts = self.repository.get_all(
                limit=limit,
                offset=offset,
                order_by=order_by,
                order_dir=order_dir,
                filtro=filtro
            )

            # Ensure precio_venta is always present
            for a in arts:
                if "precio_venta" not in a or a.get("precio_venta") is None:
                    a["precio_venta"] = 0.0

            return arts
        except Exception as e:
            logger.exception("Error getting articles: %s", e)
            return []

    def get_current_article(self) -> Optional[Dict]:
        """Obtener el artículo actualmente cargado."""
        return self.current_article

    def count_articles(self, filtro: str = "") -> int:
        """Contar artículos."""
        try:
            return self.repository.count_all(filtro)
        except Exception as e:
            logger.exception("Error counting articles: %s", e)
            return 0

    # ==================== Tarifas ====================

    def get_tarifas_for_article(self) -> List[Dict]:
        """Obtener tarifas del artículo actual."""
        if not self.current_article:
            return []

        try:
            return self.repository.get_tarifas(self.current_article["id"])
        except Exception as e:
            logger.exception("Error getting tarifas: %s", e)
            return []

    def update_tarifa(self, tarifa_id: int, data: Dict) -> bool:
        """Actualizar una tarifa."""
        try:
            return self.repository.update_tarifa(tarifa_id, data)
        except Exception as e:
            logger.exception("Error updating tarifa: %s", e)
            return False

    # ==================== Promociones ====================

    def get_ofertas_for_article(self) -> List[Dict]:
        """Obtener promociones del artículo actual."""
        if not self.current_article:
            return []

        try:
            return self.repository.get_promociones(self.current_article["id"])
        except Exception as e:
            logger.exception("Error getting promociones: %s", e)
            return []

    def save_oferta(self, oferta_data: Dict) -> Tuple[bool, str]:
        """Guardar una promoción (crear o actualizar)."""
        if not self.current_article:
            return False, "No hay artículo cargado"

        try:
            oferta_id = oferta_data.get("id")

            # Ensure articulo_id is set
            if "id_articulo" not in oferta_data:
                oferta_data["id_articulo"] = self.current_article["id"]

            if oferta_id:
                # Update existing
                success = self.repository.update_promocion(oferta_id, oferta_data)
                msg = "Promoción actualizada" if success else "Error al actualizar"
            else:
                # Create new
                new_id = self.repository.create_promocion(oferta_data)
                success = new_id is not None
                msg = "Promoción creada" if success else "Error al crear"

            return success, msg

        except Exception as e:
            logger.exception("Error saving oferta: %s", e)
            return False, f"Error: {str(e)}"

    def delete_oferta(self, oferta_id: int) -> bool:
        """Eliminar una promoción."""
        try:
            return self.repository.delete_promocion(oferta_id)
        except Exception as e:
            logger.exception("Error deleting oferta: %s", e)
            return False

    def undo_oferta(self):
        """Placeholder for undo oferta (recargar desde BD)."""
        pass

    # ==================== Lookups ====================

    def get_secciones(self) -> List[Dict]:
        """Obtener todas las secciones."""
        try:
            return self.repository.get_secciones()
        except Exception as e:
            logger.exception("Error getting secciones: %s", e)
            return []

    def get_familias(self, id_seccion: int = None) -> List[Dict]:
        """Obtener familias, opcionalmente filtradas por sección."""
        try:
            return self.repository.get_familias(id_seccion)
        except Exception as e:
            logger.exception("Error getting familias: %s", e)
            return []

    def get_subfamilias(self, id_familia: int = None) -> List[Dict]:
        """Obtener subfamilias, opcionalmente filtradas por familia."""
        try:
            return self.repository.get_subfamilias(id_familia)
        except Exception as e:
            logger.exception("Error getting subfamilias: %s", e)
            return []

    def get_tipos(self) -> List[Dict]:
        """Obtener todos los tipos de artículo."""
        try:
            return self.repository.get_tipos()
        except Exception as e:
            logger.exception("Error getting tipos: %s", e)
            return []

