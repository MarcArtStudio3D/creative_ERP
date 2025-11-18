"""
Modelos de datos para el módulo de Clientes
Basado en la estructura original de RedFox SGC (clientes.cpp)
"""

from sqlalchemy import Integer, String, Float, Date, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date
from typing import Optional
from core.db import Base


class Cliente(Base):
    """Modelo de Cliente - Refleja la estructura de RedFox SGC"""
    __tablename__ = 'clientes'
    
    # Identificadores
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_web: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    codigo_cliente: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    
    # Datos personales
    apellido1: Mapped[Optional[str]] = mapped_column(String(100))
    apellido2: Mapped[Optional[str]] = mapped_column(String(100))
    nombre: Mapped[Optional[str]] = mapped_column(String(100))
    nombre_fiscal: Mapped[Optional[str]] = mapped_column(String(200))
    nombre_comercial: Mapped[Optional[str]] = mapped_column(String(200))
    persona_contacto: Mapped[Optional[str]] = mapped_column(String(200))
    
    # Identificación fiscal
    cif_nif_siren: Mapped[Optional[str]] = mapped_column(String(50))
    siret: Mapped[Optional[str]] = mapped_column(String(14))
    cif_vies: Mapped[Optional[str]] = mapped_column(String(50))  # NIF intracomunitario
    
    # Dirección principal
    direccion1: Mapped[Optional[str]] = mapped_column(String(255))
    direccion2: Mapped[Optional[str]] = mapped_column(String(255))
    cp: Mapped[Optional[str]] = mapped_column(String(10))
    poblacion: Mapped[Optional[str]] = mapped_column(String(100))
    provincia: Mapped[Optional[str]] = mapped_column(String(100))
    id_pais: Mapped[int] = mapped_column(Integer, default=1)
    
    # Contacto
    telefono1: Mapped[Optional[str]] = mapped_column(String(50))
    telefono2: Mapped[Optional[str]] = mapped_column(String(50))
    fax: Mapped[Optional[str]] = mapped_column(String(50))
    movil: Mapped[Optional[str]] = mapped_column(String(50))
    email: Mapped[Optional[str]] = mapped_column(String(200))
    web: Mapped[Optional[str]] = mapped_column(String(200))
    
    # Fechas importantes
    fecha_alta: Mapped[date] = mapped_column(Date, default=date.today)
    fecha_ultima_compra: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    fecha_nacimiento: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    # Estadísticas
    acumulado_ventas: Mapped[float] = mapped_column(Float, default=0.0)
    ventas_ejercicio: Mapped[float] = mapped_column(Float, default=0.0)
    riesgo_maximo: Mapped[float] = mapped_column(Float, default=0.0)
    deuda_actual: Mapped[float] = mapped_column(Float, default=0.0)
    importe_pendiente: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Comentarios y bloqueos
    comentarios: Mapped[Optional[str]] = mapped_column(Text)
    bloqueado: Mapped[bool] = mapped_column(Boolean, default=False)
    comentario_bloqueo: Mapped[Optional[str]] = mapped_column(Text)
    observaciones: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Datos financieros
    porc_dto_cliente: Mapped[float] = mapped_column(Float, default=0.0)  # Porcentaje descuento fijo
    recargo_equivalencia: Mapped[bool] = mapped_column(Boolean, default=False)
    irpf: Mapped[bool] = mapped_column(Boolean, default=False)  # Cliente empresa (aplicar IRPF)
    grupo_iva: Mapped[int] = mapped_column(Integer, default=1)  # 1=General, 2=UE, 3=Exento, 4=Exportación
    
    # Contabilidad (PGC)
    cuenta_contable: Mapped[Optional[str]] = mapped_column(String(50))
    cuenta_iva_repercutido: Mapped[Optional[str]] = mapped_column(String(50))
    cuenta_deudas: Mapped[Optional[str]] = mapped_column(String(50))
    cuenta_cobros: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Forma de pago
    id_forma_pago: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    dia_pago1: Mapped[int] = mapped_column(Integer, default=0)
    dia_pago2: Mapped[int] = mapped_column(Integer, default=0)
    
    # Datos bancarios
    entidad_bancaria: Mapped[Optional[str]] = mapped_column(String(4))
    oficina_bancaria: Mapped[Optional[str]] = mapped_column(String(4))
    dc: Mapped[Optional[str]] = mapped_column(String(2))
    cuenta_corriente: Mapped[Optional[str]] = mapped_column(String(10))
    
    # Importes especiales
    importe_a_cuenta: Mapped[float] = mapped_column(Float, default=0.0)
    vales: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Tarjetas de crédito
    visa_distancia1: Mapped[Optional[str]] = mapped_column(String(20))
    visa_distancia2: Mapped[Optional[str]] = mapped_column(String(20))
    visa1_caduca_mes: Mapped[int] = mapped_column(Integer, default=0)
    visa2_caduca_mes: Mapped[int] = mapped_column(Integer, default=0)
    visa1_caduca_ano: Mapped[int] = mapped_column(Integer, default=0)
    visa2_caduca_ano: Mapped[int] = mapped_column(Integer, default=0)
    visa1_cod_valid: Mapped[int] = mapped_column(Integer, default=0)
    visa2_cod_valid: Mapped[int] = mapped_column(Integer, default=0)
    
    # Acceso web
    acceso_web: Mapped[Optional[str]] = mapped_column(String(100))
    password_web: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Referencias a otras tablas
    id_tarifa: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # Tarifa de precios
    id_divisa: Mapped[int] = mapped_column(Integer, default=1)  # Divisa predeterminada
    id_idioma_documentos: Mapped[int] = mapped_column(Integer, default=1)  # Idioma para documentos
    id_agente: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # Agente comercial
    id_transportista: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # Transportista predeterminado
    
    def __repr__(self):
        return f"<Cliente(id={self.id}, codigo='{self.codigo_cliente}', nombre='{self.nombre_fiscal}')>"
    
    def nombre_completo(self):
        """Devuelve el nombre completo del cliente"""
        nombre_fiscal = self.nombre_fiscal
        if nombre_fiscal:
            return nombre_fiscal
        nombre = self.nombre
        apellido1 = self.apellido1
        apellido2 = self.apellido2
        if nombre or apellido1:
            partes = []
            if nombre:
                partes.append(nombre)
            if apellido1:
                partes.append(apellido1)
            if apellido2:
                partes.append(apellido2)
            return " ".join(partes)
        else:
            nombre_comercial = self.nombre_comercial
            codigo_cliente = self.codigo_cliente
            return nombre_comercial or codigo_cliente
    
    def direccion_completa(self):
        """Devuelve la dirección completa formateada"""
        partes = []
        direccion1 = self.direccion1
        direccion2 = self.direccion2
        cp = self.cp
        poblacion = self.poblacion
        provincia = self.provincia
        if direccion1:
            partes.append(direccion1)
        if direccion2:
            partes.append(direccion2)
        if cp or poblacion:
            linea_ciudad = []
            if cp:
                linea_ciudad.append(cp)
            if poblacion:
                linea_ciudad.append(poblacion)
            partes.append(" ".join(linea_ciudad))
        if provincia:
            partes.append(provincia)
        return ", ".join(partes)
    
    def to_dict(self):
        """Convierte el cliente a un diccionario"""
        return {
            'id': self.id,
            'codigo_cliente': self.codigo_cliente,
            'nombre_fiscal': self.nombre_fiscal,
            'nombre_comercial': self.nombre_comercial,
            'cif_nif_siren': self.cif_nif_siren,
            'siret': self.siret,
            'direccion1': self.direccion1,
            'cp': self.cp,
            'poblacion': self.poblacion,
            'telefono1': self.telefono1,
            'email': self.email,
            'deuda_actual': self.deuda_actual,
        }


class DireccionAlternativa(Base):
    """Direcciones alternativas de entrega/facturación"""
    __tablename__ = 'direcciones_alternativas'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_cliente: Mapped[int] = mapped_column(Integer, ForeignKey('clientes.id'), nullable=False)
    
    descripcion: Mapped[Optional[str]] = mapped_column(String(100))  # Ej: "Almacén principal", "Oficina central"
    direccion1: Mapped[Optional[str]] = mapped_column(String(255))
    direccion2: Mapped[Optional[str]] = mapped_column(String(255))
    cp: Mapped[Optional[str]] = mapped_column(String(10))
    poblacion: Mapped[Optional[str]] = mapped_column(String(100))
    provincia: Mapped[Optional[str]] = mapped_column(String(100))
    id_pais: Mapped[int] = mapped_column(Integer, default=1)
    email: Mapped[Optional[str]] = mapped_column(String(200))
    comentarios: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relación con cliente
    # cliente = relationship("Cliente", back_populates="direcciones")


class DeudaCliente(Base):
    """Gestión de deudas del cliente (facturas pendientes)"""
    __tablename__ = 'deudas_clientes'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_cliente: Mapped[int] = mapped_column(Integer, ForeignKey('clientes.id'), nullable=False)
    
    fecha_deuda: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_vencimiento: Mapped[date] = mapped_column(Date, nullable=False)
    documento: Mapped[Optional[str]] = mapped_column(String(50))  # Número de factura/documento
    id_documento: Mapped[Optional[int]] = mapped_column(Integer)  # ID del documento (factura, ticket, etc.)
    tipo_documento: Mapped[Optional[str]] = mapped_column(String(20))  # 'factura', 'ticket', 'albaran'
    
    importe_total: Mapped[float] = mapped_column(Float, nullable=False)
    importe_pagado: Mapped[float] = mapped_column(Float, default=0.0)
    importe_pendiente: Mapped[float] = mapped_column(Float, nullable=False)
    
    pagado: Mapped[bool] = mapped_column(Boolean, default=False)
    fecha_pago: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    observaciones: Mapped[Optional[str]] = mapped_column(Text)


class HistorialCliente(Base):
    """Historial de operaciones con el cliente"""
    __tablename__ = 'historial_clientes'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_cliente: Mapped[int] = mapped_column(Integer, ForeignKey('clientes.id'), nullable=False)
    
    fecha: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)
    tipo_operacion: Mapped[Optional[str]] = mapped_column(String(50))  # 'venta', 'cobro', 'devolucion', 'nota'
    documento: Mapped[Optional[str]] = mapped_column(String(50))
    id_documento: Mapped[Optional[int]] = mapped_column(Integer)
    
    importe: Mapped[float] = mapped_column(Float, default=0.0)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    usuario: Mapped[Optional[str]] = mapped_column(String(100))  # Usuario que realizó la operación


class EstadisticaClienteMes(Base):
    """Estadísticas de ventas por mes"""
    __tablename__ = 'estadisticas_clientes_mes'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_cliente: Mapped[int] = mapped_column(Integer, ForeignKey('clientes.id'), nullable=False)
    
    anio: Mapped[int] = mapped_column(Integer, nullable=False)
    mes: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-12
    
    importe_ventas: Mapped[float] = mapped_column(Float, default=0.0)
    numero_operaciones: Mapped[int] = mapped_column(Integer, default=0)
    
    # Índice único para evitar duplicados
    __table_args__ = (
        {'sqlite_autoincrement': True},
    )


class Ville(Base):
    """Modelo para ciudades francesas de la base de datos france.db"""
    __tablename__ = 'villes'

    # Clave primaria: código INSEE (único para cada comuna en Francia)
    code_insee: Mapped[str] = mapped_column(String(10), primary_key=True)

    # Identificadores adicionales
    code_postal: Mapped[Optional[str]] = mapped_column(String(10))
    codes_postaux: Mapped[Optional[str]] = mapped_column(Text)  # Puede contener múltiples códigos separados

    # Nombres de la ciudad
    nom_standard: Mapped[Optional[str]] = mapped_column(String(255))
    nom_standard_majuscule: Mapped[Optional[str]] = mapped_column(String(255))

    # Región
    reg_code: Mapped[Optional[str]] = mapped_column(String(10))
    reg_nom: Mapped[Optional[str]] = mapped_column(String(255))

    # Departamento
    dep_code: Mapped[Optional[str]] = mapped_column(String(10))
    dep_nom: Mapped[Optional[str]] = mapped_column(String(255))

    # Cantón
    canton_code: Mapped[Optional[str]] = mapped_column(String(10))
    canton_nom: Mapped[Optional[str]] = mapped_column(String(255))

    # Nombres de la ciudad
    nom_standard: Mapped[Optional[str]] = mapped_column(String(255))
    nom_standard_majuscule: Mapped[Optional[str]] = mapped_column(String(255))

    # Región
    reg_code: Mapped[Optional[str]] = mapped_column(String(10))
    reg_nom: Mapped[Optional[str]] = mapped_column(String(255))

    # Departamento
    dep_code: Mapped[Optional[str]] = mapped_column(String(10))
    dep_nom: Mapped[Optional[str]] = mapped_column(String(255))

    # Cantón
    canton_code: Mapped[Optional[str]] = mapped_column(String(10))
    canton_nom: Mapped[Optional[str]] = mapped_column(String(255))

    def __repr__(self):
        return f"<Ville(code_postal='{self.code_postal}', nom_standard='{self.nom_standard}')>"

    def nombre_completo(self):
        """Devuelve el nombre completo de la ciudad"""
        return self.nom_standard or self.nom_standard_majuscule or "Sin nombre"
