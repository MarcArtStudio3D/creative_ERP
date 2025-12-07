"""
Modelos de datos para el módulo de Tipos de Cliente
Basado en la estructura original de RedFox SGC (frmtipocliente.cpp)
"""

from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional, List
from core.db import Base


class TipoCliente(Base):
    """
    Modelo de Tipo de Cliente
    Representa las categorías principales de clientes
    """
    __tablename__ = 'tipocliente_def'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    desc: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relación con subtipos
    subtipos: Mapped[List["TipoSubCliente"]] = relationship(
        "TipoSubCliente",
        back_populates="tipo",
        cascade="all, delete-orphan"
    )
    
    __table_args__ = (
        {'sqlite_autoincrement': True},
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


class TipoSubCliente(Base):
    """
    Modelo de Subtipo de Cliente
    Representa subcategorías dentro de un tipo de cliente
    """
    __tablename__ = 'tiposubcliente_def'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_tipocliente: Mapped[int] = mapped_column(Integer, ForeignKey('tipocliente_def.id'), nullable=False)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    desc: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relación con tipo padre
    tipo: Mapped["TipoCliente"] = relationship(
        "TipoCliente",
        back_populates="subtipos"
    )
    
    __table_args__ = (
        {'sqlite_autoincrement': True},
    )
    
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
