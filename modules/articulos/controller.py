from typing import Optional, Dict, Any, List
from datetime import date
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
        Initialize a new article
        Returns True if successful
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
        except Exception as e:
            print(f"Error creating article: {e}")
            return False
    
    def load_by_id(self, articulo_id: int) -> bool:
        """Load article by ID"""
        try:
            article = self.repository.get_by_id(articulo_id)
            if article:
                self.current_article = article
                self.is_new = False
                self.codigo_anterior = article.get("codigo")
                return True
            return False
        except Exception as e:
            print(f"Error loading article: {e}")
            return False
    
    def get_secciones_sql(self) -> str:
        """Get SQL for sections lookup"""
        return self.repository.get_secciones_for_lookup()
    
    def set_seccion_from_lookup(self, seccion_id: int, seccion_codigo: str, seccion_nombre: str) -> bool:
        """Set section from lookup selection"""
        try:
            if not self.current_article:
                return False
            
            # Update current article data
            self.current_article['id_seccion'] = seccion_id
            # Changing section invalidates family/subfamily selection -> clear them
            self.current_article['id_familia'] = None
            self.current_article['id_subfamilia'] = None
            
            # Return success - the view will update the display fields
            return True
        except Exception as e:
            print(f"Error setting section: {e}")
            return False
    
    def get_secciones_data(self) -> list:
        """Get sections data for lookup dialog"""
        try:
            return self.repository.get_secciones_data()
        except Exception as e:
            print(f"Error getting sections data: {e}")
            return []

    def set_familia_from_lookup(self, familia_id: int, familia_codigo: str, familia_nombre: str) -> bool:
        """Establece la familia seleccionada desde el diálogo de búsqueda (MVC: sólo actualiza el modelo)."""
        try:
            if not self.current_article:
                return False

            # Update current article data with selected family id
            self.current_article['id_familia'] = familia_id
            # Changing family invalidates subfamily selection
            self.current_article['id_subfamilia'] = None
            return True
        except Exception as e:
            print(f"Error setting familia: {e}")
            return False

    def get_familias_data(self, id_seccion: int = None) -> list:
        """Obtiene la lista de familias para el diálogo de búsqueda.
        Si se pasa id_seccion, filtra familias pertenecientes a esa sección.
        """
        try:
            return self.repository.get_familias_data(id_seccion)
        except Exception as e:
            print(f"Error getting familias data: {e}")
            return []
    
    def next_article(self) -> bool:
        """Navigate to next article"""
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
            print(f"Error navigating to next article: {e}")
            return False
    
    def prev_article(self) -> bool:
        """Navigate to previous article"""
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
            print(f"Error navigating to previous article: {e}")
            return False
    
    def save(self, form_data: Dict[str, Any]) -> tuple[bool, str]:
        """
        Save article with form data
        Returns (success, message)
        """
        if not self.current_article:
            return False, "No article loaded"
        
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
                exclude_id=self.current_article["id"]
            )
            
            if existing:
                return False, f"Ya existe un artículo con ese código, código de barras o código de fabricante: {existing.get('descripcion_reducida', '')}"
            
            # Generate slug from description
            if "descripcion_reducida" in form_data:
                form_data["slug"] = self._slugify(form_data["descripcion_reducida"])
            
            # Update article
            success = self.repository.update(self.current_article["id"], form_data)
            
            if success:
                # Reload article to get updated data
                self.current_article = self.repository.get_by_id(self.current_article["id"])
                self.is_new = False
                return True, "Artículo guardado correctamente"
            else:
                return False, "Error al guardar el artículo"
                
        except Exception as e:
            return False, f"Error al guardar: {str(e)}"
    
    def delete(self) -> tuple[bool, str]:
        """
        Delete current article
        Returns (success, message)
        """
        if not self.current_article:
            return False, "No hay artículo seleccionado"
        
        try:
            # Check if article is part of any kit
            # TODO: Implement kit check when kits are added
            
            article_id = self.current_article["id"]
            success = self.repository.delete(article_id)
            
            if success:
                # Try to load next article, or previous if no next
                if not self.next_article():
                    self.prev_article()
                
                return True, "Artículo borrado correctamente"
            else:
                return False, "Error al borrar el artículo"
                
        except Exception as e:
            return False, f"Error al borrar: {str(e)}"
    
    def clear(self):
        """Clear current article"""
        self.current_article = None
        self.is_new = False
        self.codigo_anterior = None
    
    # ==================== Validation ====================
    
    def _validate_form_data(self, form_data: Dict[str, Any]) -> Optional[str]:
        """
        Validate form data
        Returns error message if validation fails, None if OK
        """
        errors = []
        
        if not form_data.get("codigo"):
            errors.append("Código de artículo")
        
        if not form_data.get("descripcion_reducida"):
            errors.append("Nombre del artículo")
        
        # Section is optional for now (TODO: implement section lookup)
        # if not form_data.get("id_seccion"):
        #     errors.append("Sección")
        
        if errors:
            return "Debe especificar los siguientes campos:\n" + "\n".join(errors)
        
        return None
    
    # ==================== Code Generation ====================
    
    def _generate_auto_code(self, form_data: Dict[str, Any]) -> str:
        """
        Generate automatic code based on section/family/subfamily
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
                prefix = prefix[:code_length - 3]
            
            # Get next sequential code
            return self.repository.get_next_code(prefix, code_length)
            
        except Exception as e:
            print(f"Error generating auto code: {e}")
            # Fallback to simple sequential number
            import random
            return f"ART{random.randint(10000, 99999)}"
    
    def _slugify(self, text: str) -> str:
        """Convert text to URL-friendly slug"""
        import re
        import unicodedata
        
        # Normalize unicode characters
        text = unicodedata.normalize('NFKD', text)
        text = text.encode('ascii', 'ignore').decode('ascii')
        
        # Convert to lowercase and replace spaces with hyphens
        text = text.lower()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        
        return text.strip('-')
    
    # ==================== Getters ====================
    
    def get_current_article(self) -> Optional[Dict[str, Any]]:
        """Get current article data"""
        return self.current_article
    
    def get_article_id(self) -> Optional[int]:
        """Get current article ID"""
        return self.current_article.get("id") if self.current_article else None
    
    def is_editing_new(self) -> bool:
        """Check if currently editing a new article"""
        return self.is_new
    
    # ==================== Lookups ====================
    
    def get_seccion_name(self, seccion_id: int) -> str:
        """Get section name"""
        return self.repository.get_seccion(seccion_id) or ""
    
    def get_familia_name(self, familia_id: int) -> str:
        """Get family name"""
        return self.repository.get_familia(familia_id) or ""
    
    def get_subfamilia_name(self, subfamilia_id: int) -> str:
        """Get subfamily name"""
        return self.repository.get_subfamilia(subfamilia_id) or ""

    def set_subfamilia_from_lookup(self, subfamilia_id: int, subfamilia_codigo: str, subfamilia_nombre: str) -> bool:
        """Establece la subfamilia seleccionada desde el diálogo de búsqueda (sólo actualiza current_article)."""
        try:
            if not self.current_article:
                return False

            self.current_article['id_subfamilia'] = subfamilia_id
            return True
        except Exception as e:
            print(f"Error setting subfamilia: {e}")
            return False

    def get_subfamilias_data(self, id_familia: int = None) -> list:
        """Obtiene la lista de subfamilias para el diálogo de búsqueda (opcionalmente filtrada por familia)."""
        try:
            return self.repository.get_subfamilias_data(id_familia)
        except Exception as e:
            print(f"Error getting subfamilias data: {e}")
            return []
    
    def get_proveedor_info(self, proveedor_id: int) -> tuple[str, str]:
        """Get provider code and name"""
        return self.repository.get_proveedor(proveedor_id)
    
    # ==================== Search ====================
    
    def search_articles(self, search_term: str, field: str = "descripcion_reducida",
                       order_by: str = "descripcion_reducida", order_dir: str = "ASC") -> list:
        """Search articles"""
        try:
            return self.repository.search(search_term, field, order_by, order_dir)
        except Exception as e:
            print(f"Error searching articles: {e}")
            return []
    
    def filter_articles(self, filter_text: str = "") -> list:
        """
        Filter articles by search term across multiple fields
        Similar to clientes.controller.cargar_clientes with filtro parameter
        
        Args:
            filter_text: Text to filter by (searches in codigo, descripcion_reducida, codigo_barras)
            
        Returns:
            List of filtered articles
        """
        try:
            if not filter_text or filter_text.strip() == "":
                # Return all articles if no filter
                return self.repository.get_all(limit=1000)
            
            # Search across multiple fields
            return self.repository.search_multi_field(filter_text.strip())
        except Exception as e:
            print(f"Error filtering articles: {e}")
            return []
    
    def get_iva_types(self, pais: str = None) -> List[dict]:
        """
        Get IVA types for populating combo boxes
        
        Args:
            pais: Optional country filter
            
        Returns:
            List of IVA types
        """
        return self.repository.get_iva_types(pais)
