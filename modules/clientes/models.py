"""
Modelos Peewee para el módulo de Clientes.
Migración completa desde SQLModel a Peewee.
"""

from peewee import (
    Model,
    AutoField,
    CharField,
    TextField,
    IntegerField,
    DecimalField,
    DateField,
)

from core.peewee_db import database_proxy


class BaseModel(Model):
    """Modelo base que usa el proxy de base de datos."""
    class Meta:
        database = database_proxy


class Cliente(BaseModel):
    """Modelo de Cliente - Refleja la estructura real de la tabla"""

    # Identificadores
    id = AutoField(primary_key=True)
    id_web = IntegerField(null=True)
    codigo_cliente = CharField(max_length=50, unique=True, index=True)

    # Datos personales
    apellido1 = CharField(max_length=100, null=True)
    apellido2 = CharField(max_length=100, null=True)
    nombre = CharField(max_length=100, null=True)
    nombre_fiscal = CharField(max_length=200, null=True)
    nombre_comercial = CharField(max_length=200, null=True)
    persona_contacto = CharField(max_length=200, null=True)

    # Identificación fiscal
    cif_nif_siren = CharField(max_length=50, null=True)
    siret = CharField(max_length=14, null=True)
    cif_vies = CharField(max_length=50, null=True)

    # Dirección principal
    direccion1 = CharField(max_length=255, null=True)
    direccion2 = CharField(max_length=255, null=True)
    cp = CharField(max_length=10, null=True)
    poblacion = CharField(max_length=100, null=True)
    provincia = CharField(max_length=100, null=True)
    pais = CharField(max_length=100, null=True)

    # Contacto
    telefono1 = CharField(max_length=50, null=True)
    telefono2 = CharField(max_length=50, null=True)
    fax = CharField(max_length=50, null=True)
    movil = CharField(max_length=50, null=True)
    email = CharField(max_length=200, null=True)
    web = CharField(max_length=200, null=True)

    # Fechas importantes
    fecha_alta = DateField(null=True)
    fecha_ultima_compra = DateField(null=True)
    fecha_nacimiento = DateField(null=True)

    # Estadísticas (usar DecimalField para coincidir con la BD)
    acumulado_ventas = DecimalField(max_digits=15, decimal_places=2, default=0.00)
    ventas_ejercicio = DecimalField(max_digits=15, decimal_places=2, default=0.00)
    riesgo_maximo = DecimalField(max_digits=15, decimal_places=2, default=0.00)
    deuda_actual = DecimalField(max_digits=15, decimal_places=2, default=0.00)
    importe_pendiente = DecimalField(max_digits=15, decimal_places=2, default=0.00)

    # Comentarios y bloqueos
    comentarios = TextField(null=True)
    bloqueado = IntegerField(default=0)  # 0/1 en la BD
    comentario_bloqueo = TextField(null=True)
    observaciones = CharField(max_length=255, null=True)

    # Datos financieros
    porc_dto_cliente = DecimalField(max_digits=5, decimal_places=2, default=0.00)
    recargo_equivalencia = IntegerField(default=0)  # 0/1 en la BD
    irpf = IntegerField(default=0)  # 0/1 en la BD
    grupo_iva = IntegerField(default=1)

    # Contabilidad (PGC)
    cuenta_contable = CharField(max_length=50, null=True)
    cuenta_iva_repercutido = CharField(max_length=50, null=True)
    cuenta_deudas = CharField(max_length=50, null=True)
    cuenta_cobros = CharField(max_length=50, null=True)

    # Forma de pago
    id_forma_pago = IntegerField(null=True)
    dia_pago1 = IntegerField(default=0)
    dia_pago2 = IntegerField(default=0)

    # Datos bancarios
    entidad_bancaria = CharField(max_length=4, null=True)
    oficina_bancaria = CharField(max_length=4, null=True)
    dc = CharField(max_length=2, null=True)
    cuenta_corriente = CharField(max_length=10, null=True)

    # Importes especiales
    importe_a_cuenta = DecimalField(max_digits=15, decimal_places=2, default=0.00)
    vales = DecimalField(max_digits=15, decimal_places=2, default=0.00)

    # Tarjetas de crédito
    visa_distancia1 = CharField(max_length=20, null=True)
    visa_distancia2 = CharField(max_length=20, null=True)
    visa1_caduca_mes = IntegerField(default=0)
    visa2_caduca_mes = IntegerField(default=0)
    visa1_caduca_ano = IntegerField(default=0)
    visa2_caduca_ano = IntegerField(default=0)
    visa1_cod_valid = IntegerField(default=0)
    visa2_cod_valid = IntegerField(default=0)

    # Acceso web
    acceso_web = CharField(max_length=100, null=True)
    password_web = CharField(max_length=100, null=True)

    # Referencias a otras tablas
    id_tarifa = IntegerField(null=True)
    id_divisa = IntegerField(default=1)
    id_idioma_documentos = IntegerField(default=1)
    id_agente = IntegerField(null=True)
    id_transportista = IntegerField(null=True)

    class Meta:
        table_name = 'clientes'

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
        return self.codigo_cliente


class DireccionAlternativa(BaseModel):
    """Modelo de Dirección Alternativa para clientes"""

    id = AutoField(primary_key=True)
    id_cliente = IntegerField(index=True)
    descripcion = CharField(max_length=100, null=True)
    direccion1 = CharField(max_length=255, null=True)
    direccion2 = CharField(max_length=255, null=True)
    cp = CharField(max_length=10, null=True)
    poblacion = CharField(max_length=100, null=True)
    provincia = CharField(max_length=100, null=True)
    pais = CharField(max_length=100, null=True)
    email = CharField(max_length=200, null=True)
    telefono = CharField(max_length=50, null=True)
    comentarios = TextField(null=True)
    fecha_creacion = DateField(null=True)
    fecha_modificacion = DateField(null=True)

    class Meta:
        table_name = 'direcciones_alternativas'
