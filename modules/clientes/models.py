"""
Modelos de datos para el módulo de Clientes
Basado en la estructura original de RedFox SGC (clientes.cpp)
"""

from sqlmodel import SQLModel, Field, Relationship
from datetime import date, datetime
from typing import Optional, List


class Cliente(SQLModel, table=True):
    """Modelo de Cliente - Refleja la estructura de RedFox SGC"""
    __tablename__ = 'clientes'
    
    # Identificadores
    id: Optional[int] = Field(default=None, primary_key=True)
    id_web: Optional[int] = None
    codigo_cliente: str = Field(max_length=50, unique=True, index=True)
    
    # Datos personales
    apellido1: Optional[str] = Field(default=None, max_length=100)
    apellido2: Optional[str] = Field(default=None, max_length=100)
    nombre: Optional[str] = Field(default=None, max_length=100)
    nombre_fiscal: Optional[str] = Field(default=None, max_length=200)
    nombre_comercial: Optional[str] = Field(default=None, max_length=200)
    persona_contacto: Optional[str] = Field(default=None, max_length=200)
    
    # Identificación fiscal
    cif_nif_siren: Optional[str] = Field(default=None, max_length=50)
    siret: Optional[str] = Field(default=None, max_length=14)
    cif_vies: Optional[str] = Field(default=None, max_length=50)  # NIF intracomunitario
    
    # Dirección principal
    direccion1: Optional[str] = Field(default=None, max_length=255)
    direccion2: Optional[str] = Field(default=None, max_length=255)
    cp: Optional[str] = Field(default=None, max_length=10)
    poblacion: Optional[str] = Field(default=None, max_length=100)
    provincia: Optional[str] = Field(default=None, max_length=100)
    pais: str = Field(default='España', max_length=100)
    
    # Contacto
    telefono1: Optional[str] = Field(default=None, max_length=50)
    telefono2: Optional[str] = Field(default=None, max_length=50)
    fax: Optional[str] = Field(default=None, max_length=50)
    movil: Optional[str] = Field(default=None, max_length=50)
    email: Optional[str] = Field(default=None, max_length=200)
    web: Optional[str] = Field(default=None, max_length=200)
    
    # Fechas importantes
    fecha_alta: date = Field(default_factory=date.today)
    fecha_ultima_compra: Optional[date] = None
    fecha_nacimiento: Optional[date] = None
    
    # Estadísticas
    acumulado_ventas: float = Field(default=0.0)
    ventas_ejercicio: float = Field(default=0.0)
    riesgo_maximo: float = Field(default=0.0)
    deuda_actual: float = Field(default=0.0)
    importe_pendiente: float = Field(default=0.0)
    
    # Comentarios y bloqueos
    comentarios: Optional[str] = None
    bloqueado: bool = Field(default=False)
    comentario_bloqueo: Optional[str] = None
    observaciones: Optional[str] = Field(default=None, max_length=255)
    
    # Datos financieros
    porc_dto_cliente: float = Field(default=0.0)  # Porcentaje descuento fijo
    recargo_equivalencia: bool = Field(default=False)
    irpf: bool = Field(default=False)  # Cliente empresa (aplicar IRPF)
    grupo_iva: int = Field(default=1)  # 1=General, 2=UE, 3=Exento, 4=Exportación
    
    # Contabilidad (PGC)
    cuenta_contable: Optional[str] = Field(default=None, max_length=50)
    cuenta_iva_repercutido: Optional[str] = Field(default=None, max_length=50)
    cuenta_deudas: Optional[str] = Field(default=None, max_length=50)
    cuenta_cobros: Optional[str] = Field(default=None, max_length=50)
    
    # Forma de pago
    id_forma_pago: Optional[int] = None
    dia_pago1: int = Field(default=0)
    dia_pago2: int = Field(default=0)
    
    # Datos bancarios
    entidad_bancaria: Optional[str] = Field(default=None, max_length=4)
    oficina_bancaria: Optional[str] = Field(default=None, max_length=4)
    dc: Optional[str] = Field(default=None, max_length=2)
    cuenta_corriente: Optional[str] = Field(default=None, max_length=10)
    
    # Importes especiales
    importe_a_cuenta: float = Field(default=0.0)
    vales: float = Field(default=0.0)
    
    # Tarjetas de crédito
    visa_distancia1: Optional[str] = Field(default=None, max_length=20)
    visa_distancia2: Optional[str] = Field(default=None, max_length=20)
    visa1_caduca_mes: int = Field(default=0)
    visa2_caduca_mes: int = Field(default=0)
    visa1_caduca_ano: int = Field(default=0)
    visa2_caduca_ano: int = Field(default=0)
    visa1_cod_valid: int = Field(default=0)
    visa2_cod_valid: int = Field(default=0)
    
    # Acceso web
    acceso_web: Optional[str] = Field(default=None, max_length=100)
    password_web: Optional[str] = Field(default=None, max_length=100)
    
    # Referencias a otras tablas
    id_tarifa: Optional[int] = None  # Tarifa de precios
    id_divisa: int = Field(default=1)  # Divisa predeterminada
    id_idioma_documentos: int = Field(default=1)  # Idioma para documentos
    id_agente: Optional[int] = None  # Agente comercial
    id_transportista: Optional[int] = None  # Transportista predeterminado
    
    def __repr__(self):
        return f"<Cliente(id={self.id}, codigo='{self.codigo_cliente}', nombre='{self.nombre_fiscal}')>"
    
    def nombre_completo(self):
        """Devuelve el nombre completo del cliente"""
        if self.nombre_fiscal:
            return self.nombre_fiscal
        if self.nombre or self.apellido1:
            partes = []
            if self.nombre:
                partes.append(self.nombre)
            if self.apellido1:
                partes.append(self.apellido1)
            if self.apellido2:
                partes.append(self.apellido2)
            return " ".join(partes)
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
            'cif_nif_siren': self.cif_nif_siren,
            'siret': self.siret,
            'direccion1': self.direccion1,
            'cp': self.cp,
            'poblacion': self.poblacion,
            'telefono1': self.telefono1,
            'email': self.email,
            'deuda_actual': self.deuda_actual,
        }


class DireccionAlternativa(SQLModel, table=True):
    """Direcciones alternativas de entrega/facturación"""
    __tablename__ = 'direcciones_alternativas'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    id_cliente: int = Field(foreign_key="clientes.id")
    
    descripcion: Optional[str] = Field(default=None, max_length=100)  # Ej: "Almacén principal", "Oficina central"
    direccion1: Optional[str] = Field(default=None, max_length=255)
    direccion2: Optional[str] = Field(default=None, max_length=255)
    cp: Optional[str] = Field(default=None, max_length=10)
    poblacion: Optional[str] = Field(default=None, max_length=100)
    provincia: Optional[str] = Field(default=None, max_length=100)
    pais: Optional[str] = Field(default='Francia', max_length=100)
    email: Optional[str] = Field(default=None, max_length=200)
    comentarios: Optional[str] = None
    
    # Fechas
    fecha_creacion: datetime = Field(default_factory=datetime.now)
    fecha_modificacion: datetime = Field(default_factory=datetime.now)


class DeudaCliente(SQLModel, table=True):
    """Gestión de deudas del cliente (facturas pendientes)"""
    __tablename__ = 'deudas_clientes'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    id_cliente: int = Field(foreign_key="clientes.id")
    
    fecha_deuda: date
    fecha_vencimiento: date
    documento: Optional[str] = Field(default=None, max_length=50)  # Número de factura/documento
    id_documento: Optional[int] = None  # ID del documento (factura, ticket, etc.)
    tipo_documento: Optional[str] = Field(default=None, max_length=20)  # 'factura', 'ticket', 'albaran'
    
    importe_total: float
    importe_pagado: float = Field(default=0.0)
    importe_pendiente: float
    
    pagado: bool = Field(default=False)
    fecha_pago: Optional[date] = None
    
    observaciones: Optional[str] = None


class HistorialCliente(SQLModel, table=True):
    """Historial de operaciones con el cliente"""
    __tablename__ = 'historial_clientes'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    id_cliente: int = Field(foreign_key="clientes.id")
    
    fecha: date = Field(default_factory=date.today)
    tipo_operacion: Optional[str] = Field(default=None, max_length=50)  # 'venta', 'cobro', 'devolucion', 'nota'
    documento: Optional[str] = Field(default=None, max_length=50)
    id_documento: Optional[int] = None
    
    importe: float = Field(default=0.0)
    descripcion: Optional[str] = None
    usuario: Optional[str] = Field(default=None, max_length=100)  # Usuario que realizó la operación


class EstadisticaClienteMes(SQLModel, table=True):
    """Estadísticas de ventas por mes"""
    __tablename__ = 'estadisticas_clientes_mes'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    id_cliente: int = Field(foreign_key="clientes.id")
    
    anio: int
    mes: int  # 1-12
    
    importe_ventas: float = Field(default=0.0)
    numero_operaciones: int = Field(default=0)


class Ville(SQLModel, table=True):
    """Modelo de ciudades francesas"""
    __tablename__ = 'villes'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    code_postal: str = Field(max_length=10, index=True)
    
    # Región
    reg_code: Optional[str] = Field(default=None, max_length=10)
    reg_nom: Optional[str] = Field(default=None, max_length=255)
    
    # Departamento
    dep_code: Optional[str] = Field(default=None, max_length=10)
    dep_nom: Optional[str] = Field(default=None, max_length=255)
    
    # Cantón
    canton_code: Optional[str] = Field(default=None, max_length=10)
    canton_nom: Optional[str] = Field(default=None, max_length=255)
    
    # Nombres de la ciudad
    nom_standard: Optional[str] = Field(default=None, max_length=255)
    nom_standard_majuscule: Optional[str] = Field(default=None, max_length=255)
    
    def __repr__(self):
        return f"<Ville(code_postal='{self.code_postal}', nom_standard='{self.nom_standard}')>"
    
    def nombre_completo(self):
        """Devuelve el nombre completo de la ciudad"""
        return self.nom_standard or self.nom_standard_majuscule or "Sin nombre"


class ClienteTipo(SQLModel, table=True):
    """Relación entre clientes y tipos de cliente"""
    __tablename__ = 'clientes_tipos'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    id_cliente: int = Field(foreign_key="clientes.id")
    id_tipo: int = Field(foreign_key="tipocliente_def.id")
    id_subtipo: Optional[int] = Field(default=None, foreign_key="tiposubcliente_def.id")

