"""
Repositorio para el módulo de Tipos de Cliente
Maneja todas las operaciones CRUD y lógica de negocio
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from sqlmodel import select
from typing import List, Optional
from modules.tipo_cliente.models import TipoCliente, TipoSubCliente


class TipoClienteRepository:
    """Repositorio para operaciones con tipos y subtipos de clientes"""
    
    def __init__(self, session: Session):
        self.session = session
    
    # ==================== OPERACIONES CON TIPOS ====================
    
    def obtener_todos_tipos(self) -> List[TipoCliente]:
        """Obtiene todos los tipos de cliente"""
        stmt = select(TipoCliente).order_by(TipoCliente.nombre)
        return self.session.exec(stmt).all()

    def obtener_tipo_por_id(self, id_tipo: int) -> Optional[TipoCliente]:
        """Obtiene un tipo de cliente por su ID"""
        return self.session.get(TipoCliente, id_tipo)

    def obtener_tipo_por_nombre(self, nombre: str) -> Optional[TipoCliente]:
        """Obtiene un tipo de cliente por su nombre"""
        stmt = select(TipoCliente).where(TipoCliente.nombre == nombre)
        return self.session.exec(stmt).first()

    def crear_tipo(self, nombre: str, desc: str = "") -> TipoCliente:
        """
        Crea un nuevo tipo de cliente
        
        Args:
            nombre: Nombre del tipo
            desc: Descripción del tipo
            
        Returns:
            El tipo creado
            
        Raises:
            ValueError: Si el nombre está vacío o ya existe
        """
        if not nombre or nombre.strip() == "":
            raise ValueError("El nombre del tipo no puede estar vacío")
        
        # Verificar si ya existe un tipo con ese nombre
        tipo_existente = self.obtener_tipo_por_nombre(nombre)
        if tipo_existente:
            raise ValueError(f"Ya existe un tipo de cliente con el nombre '{nombre}'")
        
        tipo = TipoCliente(
            nombre=nombre.strip(),
            desc=desc.strip() if desc else None
        )
        
        self.session.add(tipo)
        self.session.commit()
        self.session.refresh(tipo)
        
        return tipo
    
    def actualizar_tipo(self, id_tipo: int, nombre: str, desc: str = "") -> TipoCliente:
        """
        Actualiza un tipo de cliente existente
        
        Args:
            id_tipo: ID del tipo a actualizar
            nombre: Nuevo nombre
            desc: Nueva descripción
            
        Returns:
            El tipo actualizado
            
        Raises:
            ValueError: Si el tipo no existe o el nombre está vacío
        """
        tipo = self.obtener_tipo_por_id(id_tipo)
        if not tipo:
            raise ValueError(f"No existe un tipo de cliente con ID {id_tipo}")
        
        if not nombre or nombre.strip() == "":
            raise ValueError("El nombre del tipo no puede estar vacío")
        
        # Verificar si otro tipo tiene el mismo nombre
        tipo_existente = self.obtener_tipo_por_nombre(nombre)
        if tipo_existente and tipo_existente.id != id_tipo:
            raise ValueError(f"Ya existe otro tipo de cliente con el nombre '{nombre}'")
        
        tipo.nombre = nombre.strip()
        tipo.desc = desc.strip() if desc else None
        
        self.session.commit()
        self.session.refresh(tipo)
        
        return tipo
    
    def eliminar_tipo(self, id_tipo: int) -> bool:
        """
        Elimina un tipo de cliente y todos sus subtipos (cascade)
        
        Args:
            id_tipo: ID del tipo a eliminar
            
        Returns:
            True si se eliminó correctamente
            
        Raises:
            ValueError: Si el tipo no existe
        """
        tipo = self.obtener_tipo_por_id(id_tipo)
        if not tipo:
            raise ValueError(f"No existe un tipo de cliente con ID {id_tipo}")
        
        # SQLAlchemy manejará el cascade delete automáticamente
        self.session.delete(tipo)
        self.session.commit()
        
        return True
    
    # ==================== OPERACIONES CON SUBTIPOS ====================
    
    def obtener_subtipos(self, id_tipo: int) -> List[TipoSubCliente]:
        """
        Obtiene todos los subtipos de un tipo de cliente específico
        
        Args:
            id_tipo: ID del tipo de cliente
            
        Returns:
            Lista de subtipos
        """
        stmt = select(TipoSubCliente).where(TipoSubCliente.id_tipocliente == id_tipo).order_by(TipoSubCliente.nombre)
        return self.session.exec(stmt).all()

    def obtener_subtipo_por_id(self, id_subtipo: int) -> Optional[TipoSubCliente]:
        """Obtiene un subtipo de cliente por su ID"""
        return self.session.get(TipoSubCliente, id_subtipo)

    def crear_subtipo(self, id_tipo: int, nombre: str, desc: str = "") -> TipoSubCliente:
        """
        Crea un nuevo subtipo de cliente
        
        Args:
            id_tipo: ID del tipo padre
            nombre: Nombre del subtipo
            desc: Descripción del subtipo
            
        Returns:
            El subtipo creado
            
        Raises:
            ValueError: Si el nombre está vacío o el tipo padre no existe
        """
        if not nombre or nombre.strip() == "":
            raise ValueError("El nombre del subtipo no puede estar vacío")
        
        # Verificar que el tipo padre existe
        tipo = self.obtener_tipo_por_id(id_tipo)
        if not tipo:
            raise ValueError(f"No existe un tipo de cliente con ID {id_tipo}")
        
        subtipo = TipoSubCliente(
            id_tipocliente=id_tipo,
            nombre=nombre.strip(),
            desc=desc.strip() if desc else None
        )
        
        self.session.add(subtipo)
        self.session.commit()
        self.session.refresh(subtipo)
        
        return subtipo
    
    def actualizar_subtipo(self, id_subtipo: int, nombre: str, desc: str = "") -> TipoSubCliente:
        """
        Actualiza un subtipo de cliente existente
        
        Args:
            id_subtipo: ID del subtipo a actualizar
            nombre: Nuevo nombre
            desc: Nueva descripción
            
        Returns:
            El subtipo actualizado
            
        Raises:
            ValueError: Si el subtipo no existe o el nombre está vacío
        """
        subtipo = self.obtener_subtipo_por_id(id_subtipo)
        if not subtipo:
            raise ValueError(f"No existe un subtipo de cliente con ID {id_subtipo}")
        
        if not nombre or nombre.strip() == "":
            raise ValueError("El nombre del subtipo no puede estar vacío")
        
        subtipo.nombre = nombre.strip()
        subtipo.desc = desc.strip() if desc else None
        
        self.session.commit()
        self.session.refresh(subtipo)
        
        return subtipo
    
    def eliminar_subtipo(self, id_subtipo: int) -> bool:
        """
        Elimina un subtipo de cliente
        
        Args:
            id_subtipo: ID del subtipo a eliminar
            
        Returns:
            True si se eliminó correctamente
            
        Raises:
            ValueError: Si el subtipo no existe
        """
        subtipo = self.obtener_subtipo_por_id(id_subtipo)
        if not subtipo:
            raise ValueError(f"No existe un subtipo de cliente con ID {id_subtipo}")
        
        self.session.delete(subtipo)
        self.session.commit()
        
        return True
    
    # ==================== OPERACIONES DE BÚSQUEDA ====================
    
    def buscar_tipos(self, termino: str) -> List[TipoCliente]:
        """
        Busca tipos de cliente por nombre o descripción
        
        Args:
            termino: Término de búsqueda
            
        Returns:
            Lista de tipos que coinciden
        """
        termino = f"%{termino}%"
        stmt = select(TipoCliente).where(
            or_(
                TipoCliente.nombre.like(termino),
                TipoCliente.desc.like(termino)
            )
        ).order_by(TipoCliente.nombre)
        return self.session.exec(stmt).all()

    def buscar_subtipos(self, termino: str, id_tipo: Optional[int] = None) -> List[TipoSubCliente]:
        """
        Busca subtipos de cliente por nombre o descripción
        
        Args:
            termino: Término de búsqueda
            id_tipo: Opcional, filtrar por tipo específico
            
        Returns:
            Lista de subtipos que coinciden
        """
        termino = f"%{termino}%"
        stmt = select(TipoSubCliente).where(
            or_(
                TipoSubCliente.nombre.like(termino),
                TipoSubCliente.desc.like(termino)
            )
        )

        if id_tipo is not None:
            stmt = stmt.where(TipoSubCliente.id_tipocliente == id_tipo)

        stmt = stmt.order_by(TipoSubCliente.nombre)
        return self.session.exec(stmt).all()
