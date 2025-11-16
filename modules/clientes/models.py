"""
Modelos de datos para el módulo de Clientes
Basado en la estructura original de RedFox SGC (clientes.cpp)
"""

from sqlalchemy import Column, Integer, String, Float, Date, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
from core.db import Base


class Cliente(Base):
    """Modelo de Cliente - Refleja la estructura de RedFox SGC"""
    __tablename__ = 'clientes'
    
    # Identificadores
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_web = Column(Integer, nullable=True)
    codigo_cliente = Column(String(50), unique=True, nullable=False)
    
    # Datos personales
    apellido1 = Column(String(100))
    apellido2 = Column(String(100))
    nombre = Column(String(100))
    nombre_fiscal = Column(String(200))
    nombre_comercial = Column(String(200))
    persona_contacto = Column(String(200))
    
    # Identificación fiscal
    cif_nif = Column(String(50))
    cif_vies = Column(String(50))  # NIF intracomunitario
    
    # Dirección principal
    direccion1 = Column(String(255))
    direccion2 = Column(String(255))
    cp = Column(String(10))
    poblacion = Column(String(100))
    provincia = Column(String(100))
    id_pais = Column(Integer, default=1)
    
    # Contacto
    telefono1 = Column(String(50))
    telefono2 = Column(String(50))
    fax = Column(String(50))
    movil = Column(String(50))
    email = Column(String(200))
    web = Column(String(200))
    
    # Fechas importantes
    fecha_alta = Column(Date, default=date.today)
    fecha_ultima_compra = Column(Date, nullable=True)
    fecha_nacimiento = Column(Date, nullable=True)
    
    # Estadísticas
    acumulado_ventas = Column(Float, default=0.0)
    ventas_ejercicio = Column(Float, default=0.0)
    riesgo_maximo = Column(Float, default=0.0)
    deuda_actual = Column(Float, default=0.0)
    importe_pendiente = Column(Float, default=0.0)
    
    # Comentarios y bloqueos
    comentarios = Column(Text)
    bloqueado = Column(Boolean, default=False)
    comentario_bloqueo = Column(Text)
    observaciones = Column(String(255))
    
    # Datos financieros
    porc_dto_cliente = Column(Float, default=0.0)  # Porcentaje descuento fijo
    recargo_equivalencia = Column(Boolean, default=False)
    irpf = Column(Boolean, default=False)  # Cliente empresa (aplicar IRPF)
    grupo_iva = Column(Integer, default=1)  # 1=General, 2=UE, 3=Exento, 4=Exportación
    
    # Contabilidad (PGC)
    cuenta_contable = Column(String(50))
    cuenta_iva_repercutido = Column(String(50))
    cuenta_deudas = Column(String(50))
    cuenta_cobros = Column(String(50))
    
    # Forma de pago
    id_forma_pago = Column(Integer, nullable=True)
    dia_pago1 = Column(Integer, default=0)
    dia_pago2 = Column(Integer, default=0)
    
    # Datos bancarios
    entidad_bancaria = Column(String(4))
    oficina_bancaria = Column(String(4))
    dc = Column(String(2))
    cuenta_corriente = Column(String(10))
    
    # Importes especiales
    importe_a_cuenta = Column(Float, default=0.0)
    vales = Column(Float, default=0.0)
    
    # Tarjetas de crédito
    visa_distancia1 = Column(String(20))
    visa_distancia2 = Column(String(20))
    visa1_caduca_mes = Column(Integer, default=0)
    visa2_caduca_mes = Column(Integer, default=0)
    visa1_caduca_ano = Column(Integer, default=0)
    visa2_caduca_ano = Column(Integer, default=0)
    visa1_cod_valid = Column(Integer, default=0)
    visa2_cod_valid = Column(Integer, default=0)
    
    # Acceso web
    acceso_web = Column(String(100))
    password_web = Column(String(100))
    
    # Referencias a otras tablas
    id_tarifa = Column(Integer, nullable=True)  # Tarifa de precios
    id_divisa = Column(Integer, default=1)  # Divisa predeterminada
    id_idioma_documentos = Column(Integer, default=1)  # Idioma para documentos
    id_agente = Column(Integer, nullable=True)  # Agente comercial
    id_transportista = Column(Integer, nullable=True)  # Transportista predeterminado
    
    def __repr__(self):
        return f"<Cliente(id={self.id}, codigo='{self.codigo_cliente}', nombre='{self.nombre_fiscal}')>"
    
    def nombre_completo(self):
        """Devuelve el nombre completo del cliente"""
        if self.nombre_fiscal:
            return self.nombre_fiscal
        elif self.nombre or self.apellido1:
            partes = []
            if self.nombre:
                partes.append(self.nombre)
            if self.apellido1:
                partes.append(self.apellido1)
            if self.apellido2:
                partes.append(self.apellido2)
            return " ".join(partes)
        else:
            return self.nombre_comercial or self.codigo_cliente
    
    def direccion_completa(self):
        """Devuelve la dirección completa formateada"""
        partes = []
        if self.direccion1:
            partes.append(self.direccion1)
        if self.direccion2:
            partes.append(self.direccion2)
        if self.cp or self.poblacion:
            linea_ciudad = []
            if self.cp:
                linea_ciudad.append(self.cp)
            if self.poblacion:
                linea_ciudad.append(self.poblacion)
            partes.append(" ".join(linea_ciudad))
        if self.provincia:
            partes.append(self.provincia)
        return ", ".join(partes)
    
    def to_dict(self):
        """Convierte el cliente a un diccionario"""
        return {
            'id': self.id,
            'codigo_cliente': self.codigo_cliente,
            'nombre_fiscal': self.nombre_fiscal,
            'nombre_comercial': self.nombre_comercial,
            'cif_nif': self.cif_nif,
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
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    
    descripcion = Column(String(100))  # Ej: "Almacén principal", "Oficina central"
    direccion1 = Column(String(255))
    direccion2 = Column(String(255))
    cp = Column(String(10))
    poblacion = Column(String(100))
    provincia = Column(String(100))
    id_pais = Column(Integer, default=1)
    email = Column(String(200))
    comentarios = Column(Text)
    
    # Relación con cliente
    # cliente = relationship("Cliente", back_populates="direcciones")


class DeudaCliente(Base):
    """Gestión de deudas del cliente (facturas pendientes)"""
    __tablename__ = 'deudas_clientes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    
    fecha_deuda = Column(Date, nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    documento = Column(String(50))  # Número de factura/documento
    id_documento = Column(Integer)  # ID del documento (factura, ticket, etc.)
    tipo_documento = Column(String(20))  # 'factura', 'ticket', 'albaran'
    
    importe_total = Column(Float, nullable=False)
    importe_pagado = Column(Float, default=0.0)
    importe_pendiente = Column(Float, nullable=False)
    
    pagado = Column(Boolean, default=False)
    fecha_pago = Column(Date, nullable=True)
    
    observaciones = Column(Text)


class HistorialCliente(Base):
    """Historial de operaciones con el cliente"""
    __tablename__ = 'historial_clientes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    
    fecha = Column(Date, nullable=False, default=date.today)
    tipo_operacion = Column(String(50))  # 'venta', 'cobro', 'devolucion', 'nota'
    documento = Column(String(50))
    id_documento = Column(Integer)
    
    importe = Column(Float, default=0.0)
    descripcion = Column(Text)
    usuario = Column(String(100))  # Usuario que realizó la operación


class EstadisticaClienteMes(Base):
    """Estadísticas de ventas por mes"""
    __tablename__ = 'estadisticas_clientes_mes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    
    anio = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)  # 1-12
    
    importe_ventas = Column(Float, default=0.0)
    numero_operaciones = Column(Integer, default=0)
    
    # Índice único para evitar duplicados
    __table_args__ = (
        {'sqlite_autoincrement': True},
    )
