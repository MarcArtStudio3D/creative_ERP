import logging
from typing import Any, Dict, List, Optional

from PySide6.QtCore import QCoreApplication

from modules.articulos.repository import ArticuloRepository


class ArticuloController:
    def __init__(self, repository: ArticuloRepository = None):
        self.repository = repository or ArticuloRepository()
        self.current_article = None
        self.is_new = False
        self.codigo_anterior = None

    # ==================== Article Lifecycle ====================

    def add_new(self) -> bool:
        """
        Inicializar un nuevo artículo.
        Devuelve True si se ha creado correctamente.
        """
        try:
            # Create article with temporary code
            new_id = self.repository.create()
            if not new_id:
                return False

            # Create tarifas for the new article
            self.repository.create_tarifas_for_article(new_id)

            # Load the new article
            self.current_article = self.repository.get_by_id(new_id)
            self.is_new = True
            self.codigo_anterior = self.current_article.get("codigo")

            return True
        except Exception:
            logging.getLogger(__name__).exception("Error creating article")
            return False

    def load_by_id(self, articulo_id: int) -> bool:
        """Cargar un artículo por su ID"""
        try:
            article = self.repository.get_by_id(articulo_id)
            if article:
                # Load base article
                self.current_article = article
                # Load offer (promocion) for this article and merge useful fields
                try:
                    oferta = self.repository.get_oferta_for_article(articulo_id)
                    if oferta:
                        # Store oferta id and unambiguous keys so UI can pick them up
                        self.current_article["oferta_id"] = oferta.get("id")
                        self.current_article["oferta_fecha_inicio"] = oferta.get(
                            "fecha_inicio"
                        )
                        self.current_article["oferta_fecha_fin"] = oferta.get(
                            "fecha_fin"
                        )
                        self.current_article["oferta_activa"] = oferta.get("activa")
                        # Additional fields
                        self.current_article["oferta_descripcion"] = oferta.get(
                            "descripcion"
                        )
                        self.current_article["oferta_unidades"] = oferta.get("unidades")
                        self.current_article["oferta_regalo"] = oferta.get("regalo")
                        self.current_article["oferta_precio_final"] = oferta.get(
                            "precio_final"
                        )
                        self.current_article["oferta_dto_local"] = oferta.get(
                            "dto_local"
                        )
                        self.current_article["oferta_dto_web"] = oferta.get("dto_web")
                        self.current_article["oferta_oferta32"] = oferta.get("oferta32")
                        self.current_article["oferta_oferta_dto"] = oferta.get(
                            "oferta_dto"
                        )
                        self.current_article["oferta_oferta_web"] = oferta.get(
                            "oferta_web"
                        )
                    else:
                        # Ensure keys exist
                        self.current_article["oferta_fecha_inicio"] = None
                        self.current_article["oferta_fecha_fin"] = None
                        self.current_article["oferta_activa"] = False
                except Exception:
                    # If oferta table is not available or other DB errors, ignore and keep base article
                    self.current_article["oferta_fecha_inicio"] = None
                    self.current_article["oferta_fecha_fin"] = None
                    self.current_article["oferta_activa"] = False
                self.is_new = False
                self.codigo_anterior = article.get("codigo")
                return True
            return False
        except Exception:
            logging.getLogger(__name__).exception("Error loading article")
            return False

    def get_secciones_sql(self) -> str:
        """Devolver la consulta SQL para el lookup de secciones"""
        return self.repository.get_secciones_for_lookup()

    def set_seccion_from_lookup(
        self, seccion_id: int, seccion_codigo: str, seccion_nombre: str
    ) -> bool:
        """Establecer la sección seleccionada desde el diálogo de búsqueda"""
        try:
            if not self.current_article:
                return False

            # Update current article data
            self.current_article["id_seccion"] = seccion_id
            # Changing section invalidates family/subfamily selection -> clear them
            self.current_article["id_familia"] = None
            self.current_article["id_subfamilia"] = None

            # Return success - the view will update the display fields
            return True
        except Exception:
            logging.getLogger(__name__).exception("Error setting section")
            return False

    def get_secciones_data(self) -> list:
        """Obtener datos de secciones para el diálogo de búsqueda"""
        try:
            return self.repository.get_secciones_data()
        except Exception:
            logging.getLogger(__name__).exception("Error getting sections data")
            return []

    # ==================== Artículo Tipo ====================
    def get_tipos_data(self) -> list:
        """Obtener lista de tipos de artículo (lookup)"""
        try:
            return self.repository.get_articulo_tipos()
        except Exception:
            logging.getLogger(__name__).exception("Error getting articulo tipos data")
            return []

    def get_tipo_by_codigo(self, codigo: str) -> dict | None:
        """Obtener un tipo de artículo por su código exacto (case-insensitive)."""
        try:
            if not codigo:
                return None
            return self.repository.get_articulo_tipo_por_codigo(codigo)
        except Exception:
            logging.getLogger(__name__).exception(
                f"Error looking up articulo tipo by codigo={codigo}"
            )
            return None

    def set_tipo_from_lookup(
        self, tipo_id: int, tipo_codigo: str, tipo_descripcion: str
    ) -> bool:
        """Establecer el tipo seleccionado en el artículo actual (no persiste hasta guardar)."""
        try:
            if not self.current_article:
                return False
            # Store both id and code/description for the view to use
            self.current_article["id_tipo"] = tipo_id
            self.current_article["codigo_tipo"] = tipo_codigo
            self.current_article["descripcion_tipo"] = tipo_descripcion
            return True
        except Exception:
            logging.getLogger(__name__).exception(
                "Error setting articulo tipo from lookup"
            )
            return False

    def set_familia_from_lookup(
        self, familia_id: int, familia_codigo: str, familia_nombre: str
    ) -> bool:
        """Establece la familia seleccionada desde el diálogo de búsqueda (MVC: sólo actualiza el modelo)."""
        try:
            if not self.current_article:
                return False

            # Update current article data with selected family id
            self.current_article["id_familia"] = familia_id
            # Changing family invalidates subfamily selection
            self.current_article["id_subfamilia"] = None
            return True
        except Exception:
            logging.getLogger(__name__).exception("Error setting familia")
            return False

    def get_familias_data(self, id_seccion: int = None) -> list:
        """Obtiene la lista de familias para el diálogo de búsqueda.
        Si se pasa id_seccion, filtra familias pertenecientes a esa sección.
        """
        try:
            return self.repository.get_familias_data(id_seccion)
        except Exception:
            logging.getLogger(__name__).exception("Error getting familias data")
            return []

    def next_article(self) -> bool:
        """Navegar al siguiente artículo"""
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
        except Exception:
            logging.getLogger(__name__).exception("Error navigating to next article")
            return False

    def prev_article(self) -> bool:
        """Navegar al artículo anterior"""
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
        except Exception:
            logging.getLogger(__name__).exception(
                "Error navigating to previous article"
            )
            return False

    def save(self, form_data: Dict[str, Any]) -> tuple[bool, str]:
        """
        Guardar un artículo usando los datos del formulario.
        Devuelve (exito: bool, mensaje: str)
        """
        if not self.current_article:
            return False, QCoreApplication.translate(
                "ArticuloController", "No article loaded"
            )

        # Validate required fields
        validation_error = self._validate_form_data(form_data)
        if validation_error:
            return False, validation_error

        try:
            # Handle auto-code generation
            codigo = form_data.get("codigo", "")
            if codigo == "auto_codigo":
                codigo = self._generate_auto_code(form_data)
                form_data["codigo"] = codigo

            # Check for duplicate codes (excluding current article)
            existing = self.repository.check_code_exists(
                codigo=form_data.get("codigo"),
                codigo_barras=form_data.get("codigo_barras"),
                codigo_fabricante=form_data.get("codigo_fabricante"),
                exclude_id=self.current_article["id"],
            )

            if existing:
                return False, QCoreApplication.translate(
                    "ArticuloController",
                    "Ya existe un artículo con ese código, código de barras o código de fabricante: {desc}",
                ).format(desc=existing.get("descripcion_reducida", ""))

            # Generate slug from description
            if "descripcion_reducida" in form_data:
                form_data["slug"] = self._slugify(form_data["descripcion_reducida"])

            # Separate out oferta (promotion) fields so we don't try to update them in articulos table
            oferta_payload = {}
            # Pull dates from form_data if present and remove them before updating articulos
            if "oferta_fecha_inicio" in form_data:
                oferta_payload["fecha_inicio"] = form_data.pop("oferta_fecha_inicio")
            if "oferta_fecha_fin" in form_data:
                oferta_payload["fecha_fin"] = form_data.pop("oferta_fecha_fin")

            # Activa flag in articulos.controls whether the oferta is active
            # Keep articulo_promocionado in article data (it's a column in articulos)

            # Update article and oferta atomically in a single transaction
            # Use a fresh Session instance (avoid scoped session which may already have an active transaction)
            from sqlalchemy.orm import sessionmaker

            from core.db import get_engine

            engine = get_engine()

            # include activa flag into oferta_payload (if present)
            if "articulo_promocionado" in form_data:
                oferta_payload["activa"] = bool(form_data.get("articulo_promocionado"))

            # Use a connection-level transaction so the update + upsert are atomic
            try:
                with engine.begin() as conn:
                    Session = sessionmaker(bind=conn, autocommit=False, autoflush=False)
                    session = Session()
                    tx_repo = ArticuloRepository(session=session)

                    tarifa_id = tx_repo.get_default_tarifa()

                    # Perform update and upsert on the same connection/session
                    success = tx_repo.update(self.current_article["id"], form_data)
                    if not success:
                        raise Exception("Error actualizando artículo")

                    if oferta_payload:
                        # Only create/insert an oferta row when there is meaningful data or an
                        # existing oferta already exists for this article+tarifa. This prevents
                        # accidental creation of empty oferta rows when saving article form
                        # that contains only None/empty placeholder keys.
                        try:
                            existing = tx_repo.get_oferta_for_article(
                                self.current_article["id"], tarifa_id
                            )
                        except Exception:
                            existing = None

                        def _meaningful(v):
                            # treat None, empty-string, False and numeric 0 as not meaningful
                            if v is None:
                                return False
                            if isinstance(v, str) and v.strip() == "":
                                return False
                            if isinstance(v, bool) and v is False:
                                return False
                            try:
                                if isinstance(v, (int, float)) and float(v) == 0.0:
                                    return False
                            except Exception:
                                pass
                            return True

                        has_meaningful = any(
                            _meaningful(val) for val in oferta_payload.values()
                        )

                        # If there is no existing oferta and there is no meaningful data, skip upsert
                        if not existing and not has_meaningful:
                            # nothing to do — avoid creating empty oferta rows
                            ok = True
                        else:
                            ok = tx_repo.upsert_oferta(
                                self.current_article["id"], tarifa_id, oferta_payload
                            )

                        if not ok:
                            raise Exception("Error guardando oferta")
            except Exception as e:
                try:
                    session.rollback()
                except Exception:
                    pass
                session.close()
                return False, QCoreApplication.translate(
                    "ArticuloController", "Error al guardar: {err}"
                ).format(err=str(e))
            finally:
                # ensure session closed if not already
                try:
                    session.close()
                except Exception:
                    pass

            if success:
                # Reload article to get updated data (includes oferta merged)
                self.current_article = self.repository.get_by_id(
                    self.current_article["id"]
                )
                # Reload oferta data and merge again
                try:
                    oferta = self.repository.get_oferta_for_article(
                        self.current_article["id"]
                    )
                    if oferta:
                        self.current_article["oferta_fecha_inicio"] = oferta.get(
                            "fecha_inicio"
                        )
                        self.current_article["oferta_fecha_fin"] = oferta.get(
                            "fecha_fin"
                        )
                        self.current_article["oferta_activa"] = oferta.get("activa")
                    else:
                        self.current_article["oferta_fecha_inicio"] = None
                        self.current_article["oferta_fecha_fin"] = None
                        self.current_article["oferta_activa"] = False
                except Exception:
                    self.current_article["oferta_fecha_inicio"] = None
                    self.current_article["oferta_fecha_fin"] = None
                    self.current_article["oferta_activa"] = False
                self.is_new = False
                return True, QCoreApplication.translate(
                    "ArticuloController", "Artículo guardado correctamente"
                )
            else:
                return False, QCoreApplication.translate(
                    "ArticuloController", "Error al guardar el artículo"
                )

        except Exception as e:
            return False, QCoreApplication.translate(
                "ArticuloController", "Error al guardar: {err}"
            ).format(err=str(e))

    def delete(self) -> tuple[bool, str]:
        """
        Eliminar el artículo actual.
        Devuelve (exito: bool, mensaje: str)
        """
        if not self.current_article:
            return False, QCoreApplication.translate(
                "ArticuloController", "No hay artículo seleccionado"
            )

        try:
            # Check if article is part of any kit
            # TODO: Implement kit check when kits are added

            article_id = self.current_article["id"]
            success = self.repository.delete(article_id)

            if success:
                # Try to load next article, or previous if no next
                if not self.next_article():
                    self.prev_article()

                return True, QCoreApplication.translate(
                    "ArticuloController", "Artículo borrado correctamente"
                )
            else:
                return False, QCoreApplication.translate(
                    "ArticuloController", "Error al borrar el artículo"
                )

        except Exception as e:
            return False, QCoreApplication.translate(
                "ArticuloController", "Error al borrar: {err}"
            ).format(err=str(e))

    def clear(self):
        """Limpiar el artículo actual en memoria (reset estado de edición)."""
        self.current_article = None
        self.is_new = False
        self.codigo_anterior = None

    # ==================== Validation ====================

    def _validate_form_data(self, form_data: Dict[str, Any]) -> Optional[str]:
        """
        Validar los datos del formulario.
        Devuelve un mensaje de error si la validación falla, o None si OK.
        """
        errors = []

        if not form_data.get("codigo"):
            errors.append(
                QCoreApplication.translate("ArticuloController", "Código de artículo")
            )

        if not form_data.get("descripcion_reducida"):
            errors.append(
                QCoreApplication.translate("ArticuloController", "Nombre del artículo")
            )

        # Section is optional for now (TODO: implement section lookup)
        # if not form_data.get("id_seccion"):
        #     errors.append("Sección")

        if errors:
            return QCoreApplication.translate(
                "ArticuloController",
                "Debe especificar los siguientes campos:\n{fields}",
            ).format(fields="\n".join(errors))

        return None

    # ==================== Code Generation ====================

    def _generate_auto_code(self, form_data: Dict[str, Any]) -> str:
        """
        Generar un código automático basado en sección/familia/subfamilia.
        """
        try:
            # Get configuration for code length
            # TODO: Get from configuration table
            code_length = 10  # Default length

            # Build prefix from section/family/subfamily codes
            prefix_parts = []

            # Get section code
            id_seccion = form_data.get("id_seccion")
            if id_seccion:
                # TODO: Get section code from database
                pass

            # Get family code
            id_familia = form_data.get("id_familia")
            if id_familia:
                # TODO: Get family code from database
                pass

            # Get subfamily code
            id_subfamilia = form_data.get("id_subfamilia")
            if id_subfamilia:
                # TODO: Get subfamily code from database
                pass

            prefix = "".join(prefix_parts)

            # Ensure prefix doesn't exceed code length - 3 (for number)
            if len(prefix) + 3 > code_length:
                prefix = prefix[: code_length - 3]

            # Get next sequential code
            return self.repository.get_next_code(prefix, code_length)

        except Exception:
            logging.getLogger(__name__).exception("Error generating auto code")
            # Fallback to simple sequential number
            import random

            return f"ART{random.randint(10000, 99999)}"

    def _slugify(self, text: str) -> str:
        """Convertir texto a un slug compatible con URLs"""
        import re
        import unicodedata

        # Normalize unicode characters
        text = unicodedata.normalize("NFKD", text)
        text = text.encode("ascii", "ignore").decode("ascii")

        # Convert to lowercase and replace spaces with hyphens
        text = text.lower()
        text = re.sub(r"[^\w\s-]", "", text)
        text = re.sub(r"[-\s]+", "-", text)

        return text.strip("-")

    # ==================== Getters ====================

    def get_current_article(self) -> Optional[Dict[str, Any]]:
        """Obtener los datos del artículo actualmente cargado"""
        return self.current_article

    def save_oferta(self, oferta_payload: Dict[str, Any]) -> tuple[bool, str]:
        """
        Guardar (insertar o actualizar) una oferta independiente para el artículo actualmente cargado.
        oferta_payload puede contener: fecha_inicio, fecha_fin, activa, descripcion, etc.

        Devuelve (success: bool, message: str)
        """
        # Debug: ensure this function is being called and current_article is present
        try:
            print("ENTER save_oferta current_article:", self.current_article)
        except Exception:
            pass
        if not self.current_article:
            return False, QCoreApplication.translate(
                "ArticuloController", "No article loaded"
            )

        try:
            from sqlalchemy.orm import sessionmaker

            from core.db import get_engine

            engine = get_engine()

            # Use a short transaction to insert or update oferta by its own id when possible
            try:
                with engine.begin() as conn:
                    Session = sessionmaker(bind=conn, autocommit=False, autoflush=False)
                    session = Session()
                    tx_repo = ArticuloRepository(session=session)

                    # If oferta id is known, update by id. Otherwise create a new oferta for this article+tarifa.
                    tarifa_id = tx_repo.get_default_tarifa()
                    oferta_id = oferta_payload.get("id") or self.current_article.get(
                        "oferta_id"
                    )

                    logging.getLogger(__name__).debug(
                        "save_oferta: oferta_id=%s tarifa=%s payload=%s",
                        oferta_id,
                        tarifa_id,
                        oferta_payload,
                    )
                    # DEBUG: imprimir payload en stdout para tests (se mostrará con -s)
                    try:
                        print(
                            "DEBUG save_oferta: oferta_id=",
                            oferta_id,
                            "tarifa=",
                            tarifa_id,
                            "payload=",
                            oferta_payload,
                        )
                    except Exception:
                        pass

                    # Sanitize descripcion in payload (protect against placeholder values like 'other')
                    try:
                        if oferta_payload and isinstance(
                            oferta_payload.get("descripcion"), str
                        ):
                            desc = oferta_payload.get("descripcion").strip()
                            if desc and desc.lower() == "other":
                                logging.getLogger(__name__).warning(
                                    "Sanitizando descripcion de oferta no válida en controlador: '%s' -> se limpia",
                                    desc,
                                )
                                oferta_payload["descripcion"] = None
                    except Exception:
                        pass

                    if oferta_id:
                        # Use upsert to update the oferta row for this article+tarifa. This is robust
                        # even if oferta_id is present or mismatched; upsert handles both update and insert
                        ok = tx_repo.upsert_oferta(
                            self.current_article["id"], tarifa_id, oferta_payload
                        )
                        logging.getLogger(__name__).debug(
                            "upsert_oferta (update path) returned: %s", ok
                        )
                        try:
                            print("DEBUG upsert returned:", ok)
                        except Exception:
                            pass
                        if not ok:
                            raise Exception("Repository upsert failed")
                    else:
                        ok = tx_repo.upsert_oferta(
                            self.current_article["id"], tarifa_id, oferta_payload
                        )
                        logging.getLogger(__name__).debug(
                            "upsert_oferta (insert path) returned: %s", ok
                        )
                        try:
                            print("DEBUG upsert returned:", ok)
                        except Exception:
                            pass
                        if not ok:
                            raise Exception("Repository upsert failed")
            except Exception as e:
                try:
                    session.rollback()
                except Exception:
                    pass
                session.close()
                return False, QCoreApplication.translate(
                    "ArticuloController", "Error guardando oferta: {err}"
                ).format(err=str(e))
            finally:
                try:
                    session.close()
                except Exception:
                    pass

            # Refresh current_article oferta fields (prefer by oferta_id)
            try:
                oferta = None
                if oferta_id:
                    oferta = self.repository.get_oferta_by_id(oferta_id)
                if not oferta:
                    oferta = self.repository.get_oferta_for_article(
                        self.current_article["id"]
                    )

                logging.getLogger(__name__).debug("Post-save fetched oferta=%s", oferta)

                if oferta:
                    self.current_article["oferta_id"] = oferta.get("id")
                    self.current_article["oferta_fecha_inicio"] = oferta.get(
                        "fecha_inicio"
                    )
                    self.current_article["oferta_fecha_fin"] = oferta.get("fecha_fin")
                    self.current_article["oferta_activa"] = oferta.get("activa")
                    self.current_article["oferta_descripcion"] = oferta.get(
                        "descripcion"
                    )
                    self.current_article["oferta_unidades"] = oferta.get("unidades")
                    self.current_article["oferta_regalo"] = oferta.get("regalo")
                    self.current_article["oferta_precio_final"] = oferta.get(
                        "precio_final"
                    )
                    self.current_article["oferta_dto_local"] = oferta.get("dto_local")
                    self.current_article["oferta_dto_web"] = oferta.get("dto_web")
                    self.current_article["oferta_oferta32"] = oferta.get("oferta32")
                    self.current_article["oferta_oferta_dto"] = oferta.get("oferta_dto")
                    self.current_article["oferta_oferta_web"] = oferta.get("oferta_web")
                else:
                    self.current_article["oferta_fecha_inicio"] = None
                    self.current_article["oferta_fecha_fin"] = None
                    self.current_article["oferta_activa"] = False
            except Exception:
                # Non-fatal: ignore refresh errors
                pass

            return True, QCoreApplication.translate(
                "ArticuloController", "Oferta guardada correctamente"
            )
        except Exception as e:
            return False, QCoreApplication.translate(
                "ArticuloController", "Error guardando oferta: {err}"
            ).format(err=str(e))

    def insert_oferta(
        self, oferta_payload: Dict[str, Any] | None = None
    ) -> tuple[bool, str, Optional[dict]]:
        """
        Create a new oferta row for the currently loaded article using oferta_payload (or defaults)
        and refresh controller.current_article oferta fields.

        Returns (success: bool, message: str)
        """
        if not self.current_article:
            return (
                False,
                QCoreApplication.translate("ArticuloController", "No article loaded"),
                None,
            )

        try:
            from sqlalchemy.orm import sessionmaker

            from core.db import get_engine

            engine = get_engine()

            try:
                with engine.begin() as conn:
                    Session = sessionmaker(bind=conn, autocommit=False, autoflush=False)
                    session = Session()
                    tx_repo = ArticuloRepository(session=session)

                    tarifa_id = tx_repo.get_default_tarifa()

                    # Sanitize payload description
                    try:
                        if oferta_payload and isinstance(
                            oferta_payload.get("descripcion"), str
                        ):
                            d = oferta_payload.get("descripcion").strip()
                            if d and d.lower() == "other":
                                logging.getLogger(__name__).warning(
                                    "Sanitizando descripcion de oferta no válida en controlador.insert_oferta: '%s' -> se limpia",
                                    d,
                                )
                                oferta_payload["descripcion"] = None
                    except Exception:
                        pass

                    row = tx_repo.insert_oferta(
                        self.current_article["id"], tarifa_id, oferta_payload or {}
                    )
                    if not row:
                        raise Exception("Repository insert failed")
                    # update current_article with new oferta id and useful fields
                    self.current_article["oferta_id"] = row.get("id")
                    self.current_article["oferta_fecha_inicio"] = row.get(
                        "fecha_inicio"
                    )
                    self.current_article["oferta_fecha_fin"] = row.get("fecha_fin")
                    self.current_article["oferta_activa"] = row.get("activa")
                    self.current_article["oferta_descripcion"] = row.get("descripcion")
                    self.current_article["oferta_unidades"] = row.get("unidades")
                    self.current_article["oferta_regalo"] = row.get("regalo")
                    self.current_article["oferta_precio_final"] = row.get(
                        "precio_final"
                    )
                    self.current_article["oferta_dto_local"] = row.get("dto_local")
                    self.current_article["oferta_dto_web"] = row.get("dto_web")
                    self.current_article["oferta_oferta32"] = row.get("oferta32")
                    self.current_article["oferta_oferta_dto"] = row.get("oferta_dto")
                    self.current_article["oferta_oferta_web"] = row.get("oferta_web")
            except Exception as e:
                try:
                    session.rollback()
                except Exception:
                    pass
                session.close()
                return (
                    False,
                    QCoreApplication.translate(
                        "ArticuloController", "Error insertando oferta: {err}"
                    ).format(err=str(e)),
                    None,
                )
            finally:
                try:
                    session.close()
                except Exception:
                    pass

            # Refresh loaded article oferta fields
            try:
                oferta = self.repository.get_oferta_for_article(
                    self.current_article["id"]
                )
                if oferta:
                    self.current_article["oferta_fecha_inicio"] = oferta.get(
                        "fecha_inicio"
                    )
                    self.current_article["oferta_fecha_fin"] = oferta.get("fecha_fin")
                    self.current_article["oferta_activa"] = oferta.get("activa")
                else:
                    self.current_article["oferta_fecha_inicio"] = None
                    self.current_article["oferta_fecha_fin"] = None
                    self.current_article["oferta_activa"] = False
            except Exception:
                pass

            return (
                True,
                QCoreApplication.translate("ArticuloController", "Oferta creada"),
                row,
            )
        except Exception as e:
            return (
                False,
                QCoreApplication.translate(
                    "ArticuloController", "Error insertando oferta: {err}"
                ).format(err=str(e)),
                None,
            )

    def delete_oferta(self) -> tuple[bool, str]:
        """
        Delete the oferta for the currently loaded article (default tarifa) and refresh controller.current_article
        """
        if not self.current_article:
            return False, QCoreApplication.translate(
                "ArticuloController", "No article loaded"
            )

        try:
            # Prefer deletion by oferta id if present
            oferta_id = self.current_article.get("oferta_id")
            if oferta_id:
                ok = self.repository.delete_oferta_by_id(oferta_id)
            else:
                tarifa_id = self.repository.get_default_tarifa()
                ok = self.repository.delete_oferta(
                    self.current_article["id"], tarifa_id
                )
            if not ok:
                return False, QCoreApplication.translate(
                    "ArticuloController", "Operación de borrado fallida"
                )

            # Clear oferta fields including id
            self.current_article["oferta_id"] = None
            self.current_article["oferta_fecha_inicio"] = None
            self.current_article["oferta_fecha_fin"] = None
            self.current_article["oferta_activa"] = False
            self.current_article["oferta_descripcion"] = None
            self.current_article["oferta_unidades"] = None
            self.current_article["oferta_regalo"] = None
            self.current_article["oferta_precio_final"] = None
            self.current_article["oferta_dto_local"] = None
            self.current_article["oferta_dto_web"] = None
            self.current_article["oferta_oferta32"] = None
            self.current_article["oferta_oferta_dto"] = None
            self.current_article["oferta_oferta_web"] = None
            return True, QCoreApplication.translate(
                "ArticuloController", "Oferta eliminada"
            )
        except Exception as e:
            return False, QCoreApplication.translate(
                "ArticuloController", "Error eliminando oferta: {err}"
            ).format(err=str(e))

    def get_article_id(self) -> Optional[int]:
        """Obtener el ID del artículo actualmente cargado"""
        return self.current_article.get("id") if self.current_article else None

    def is_editing_new(self) -> bool:
        """Comprobar si se está editando un artículo nuevo (no persistido)"""
        return self.is_new

    # ==================== Lookups ====================

    def get_seccion_name(self, seccion_id: int) -> str:
        """Obtener el nombre de la sección"""
        return self.repository.get_seccion(seccion_id) or ""

    def get_familia_name(self, familia_id: int) -> str:
        """Obtener el nombre de la familia"""
        return self.repository.get_familia(familia_id) or ""

    def get_subfamilia_name(self, subfamilia_id: int) -> str:
        """Obtener el nombre de la subfamilia"""
        return self.repository.get_subfamilia(subfamilia_id) or ""

    def set_subfamilia_from_lookup(
        self, subfamilia_id: int, subfamilia_codigo: str, subfamilia_nombre: str
    ) -> bool:
        """Establece la subfamilia seleccionada desde el diálogo de búsqueda (sólo actualiza current_article)."""
        try:
            if not self.current_article:
                return False

            self.current_article["id_subfamilia"] = subfamilia_id
            return True
        except Exception:
            logging.getLogger(__name__).exception("Error setting subfamilia")
            return False

    def get_subfamilias_data(self, id_familia: int = None) -> list:
        """Obtiene la lista de subfamilias para el diálogo de búsqueda (opcionalmente filtrada por familia)."""
        try:
            return self.repository.get_subfamilias_data(id_familia)
        except Exception:
            logging.getLogger(__name__).exception("Error getting subfamilias data")
            return []

    def get_proveedor_info(self, proveedor_id: int) -> tuple[str, str]:
        """Obtener código y nombre del proveedor"""
        return self.repository.get_proveedor(proveedor_id)

    # ==================== Search ====================

    def search_articles(
        self,
        search_term: str,
        field: str = "descripcion_reducida",
        order_by: str = "descripcion_reducida",
        order_dir: str = "ASC",
    ) -> list:
        """Buscar artículos (búsqueda parametrizada)"""
        try:
            return self.repository.search(search_term, field, order_by, order_dir)
        except Exception:
            logging.getLogger(__name__).exception("Error searching articles")
            return []

    def filter_articles(self, filter_text: str = "") -> list:
        """
        Filtrar artículos por término de búsqueda en varios campos.
        Similar a clientes.controller.cargar_clientes con parámetro filtro.

        Args:
            filter_text: Texto a filtrar (busca en codigo, descripcion_reducida, codigo_barras)

        Returns:
            Lista de artículos filtrados
        """
        try:
            if not filter_text or filter_text.strip() == "":
                # Return all articles if no filter
                return self.repository.get_all(limit=1000)

            # Search across multiple fields
            return self.repository.search_multi_field(filter_text.strip())
        except Exception:
            logging.getLogger(__name__).exception("Error filtering articles")
            return []

    def get_iva_types(self, pais: str = None) -> List[dict]:
        """
        Obtener tipos de IVA para rellenar comboboxes.

        Args:
            pais: Filtro de país opcional

        Returns:
            Lista de tipos de IVA
        """
        return self.repository.get_iva_types(pais)
