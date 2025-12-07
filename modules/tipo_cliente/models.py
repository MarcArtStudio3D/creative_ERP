"""
Modelos de datos para el módulo de Tipos de Cliente
Basado en la estructura original de RedFox SGC (frmtipocliente.cpp)
"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class TipoCliente(SQLModel, table=True):
    """
    Modelo de Tipo de Cliente
    Representa las categorías principales de clientes
    """
    __tablename__ = 'tipocliente_def'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    desc: Optional[str] = Field(default=None)

    # Relación con subtipos
    subtipos: List["TipoSubCliente"] = Relationship(
        back_populates="tipo",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    
    def __repr__(self):
        return f"<TipoCliente(id={self.id}, nombre='{self.nombre}')>"
    
    def to_dict(self):
        """Convierte el tipo de cliente a un diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'desc': self.desc,
            'num_subtipos': len(self.subtipos) if self.subtipos else 0
        }


class TipoSubCliente(SQLModel, table=True):
    """
    Modelo de Subtipo de Cliente
    Representa subcategorías dentro de un tipo de cliente
    """
    __tablename__ = 'tiposubcliente_def'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    id_tipocliente: int = Field(foreign_key="tipocliente_def.id")
    nombre: str = Field(max_length=100)
    desc: Optional[str] = Field(default=None)

    # Relación con tipo padre
    tipo: Optional[TipoCliente] = Relationship(back_populates="subtipos")

    def __repr__(self):
        return f"<TipoSubCliente(id={self.id}, nombre='{self.nombre}', id_tipocliente={self.id_tipocliente})>"
    
    def to_dict(self):
        """Convierte el subtipo de cliente a un diccionario"""
        return {
            'id': self.id,
            'id_tipocliente': self.id_tipocliente,
            'nombre': self.nombre,
            'desc': self.desc,
            'tipo_nombre': self.tipo.nombre if self.tipo else None
        }
