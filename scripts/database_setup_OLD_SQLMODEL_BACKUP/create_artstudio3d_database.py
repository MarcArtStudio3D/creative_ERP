#!/usr/bin/env python3
"""
Script para crear la base de datos 'ArtStudio3D'
y migrar las tablas específicas: clientes, tipocliente_def, tiposubcliente_def
"""

import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))


def create_artstudio3d_database():
    """Crea la base de datos 'ArtStudio3D' y migra las tablas específicas."""

    print("Creating ArtStudio3D database...")

    # Configuración de la nueva base de datos ArtStudio3D
    artstudio_db_url = os.environ.get(
        "ARTSTUDIO3D_DB", "mysql+pymysql://admin:admin123@127.0.0.1:3306/artstudio3d"
    )

    # Configuración de la base de datos actual
    current_db_url = os.environ.get(
        "CREATIVE_ERP_CURRENT_DB",
        "mysql+pymysql://admin:admin123@127.0.0.1:3306/creative_erp",
    )

    try:
        from sqlalchemy import MetaData, text

        from core.db import get_engine_from_url

        # Primero crear la base de datos conectándose sin especificar BD
        temp_url = "mysql+pymysql://admin:admin123@127.0.0.1:3306"
        temp_engine = get_engine_from_url(temp_url)

        # Crear la base de datos si no existe
        with temp_engine.connect() as conn:
            conn.execute(text("CREATE DATABASE IF NOT EXISTS artstudio3d"))
            conn.commit()

        temp_engine.dispose()

        # Ahora conectarse a la base de datos específica
        artstudio_engine = get_engine_from_url(artstudio_db_url)
        MetaData()

        # Crear motor para la base de datos actual
        current_engine = get_engine_from_url(current_db_url)

        # Crear tablas específicas en la nueva base de datos
        print("Creating specific tables...")

        # Tabla tipocliente_def
        with artstudio_engine.connect() as conn:
            conn.execute(
                text(
                    """
                CREATE TABLE IF NOT EXISTS tipocliente_def (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    nombre VARCHAR(100) NOT NULL,
                    `desc` TEXT
                )
            """
                )
            )

            # Tabla tiposubcliente_def
            conn.execute(
                text(
                    """
                CREATE TABLE IF NOT EXISTS tiposubcliente_def (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    id_tipocliente INTEGER NOT NULL,
                    nombre VARCHAR(100) NOT NULL,
                    `desc` TEXT,
                    FOREIGN KEY (id_tipocliente) REFERENCES tipocliente_def(id)
                )
            """
                )
            )

            # Tabla clientes (basada en el modelo de clientes)
            conn.execute(
                text(
                    """
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    id_web INTEGER,
                    codigo_cliente VARCHAR(50) UNIQUE NOT NULL,
                    apellido1 VARCHAR(100),
                    apellido2 VARCHAR(100),
                    nombre VARCHAR(100),
                    nombre_fiscal VARCHAR(200),
                    nombre_comercial VARCHAR(200),
                    persona_contacto VARCHAR(200),
                    cif_nif_siren VARCHAR(50),
                    siret VARCHAR(14),
                    cif_vies VARCHAR(50),
                    direccion1 VARCHAR(255),
                    direccion2 VARCHAR(255),
                    cp VARCHAR(10),
                    poblacion VARCHAR(100),
                    provincia VARCHAR(100),
                    id_pais VARCHAR(100) DEFAULT 'España',
                    telefono1 VARCHAR(50),
                    telefono2 VARCHAR(50),
                    fax VARCHAR(50),
                    movil VARCHAR(50),
                    email VARCHAR(200),
                    web VARCHAR(200),
                    fecha_alta DATE DEFAULT CURRENT_DATE,
                    fecha_ultima_compra DATE,
                    fecha_nacimiento DATE,
                    acumulado_ventas DECIMAL(15,2) DEFAULT 0.00,
                    ventas_ejercicio DECIMAL(15,2) DEFAULT 0.00,
                    riesgo_maximo DECIMAL(15,2) DEFAULT 0.00,
                    deuda_actual DECIMAL(15,2) DEFAULT 0.00,
                    importe_pendiente DECIMAL(15,2) DEFAULT 0.00,
                    comentarios TEXT,
                    bloqueado INTEGER DEFAULT 0,
                    comentario_bloqueo TEXT,
                    observaciones VARCHAR(255),
                    porc_dto_cliente DECIMAL(5,2) DEFAULT 0.00,
                    recargo_equivalencia INTEGER DEFAULT 0,
                    irpf INTEGER DEFAULT 0,
                    grupo_iva INTEGER DEFAULT 1,
                    cuenta_contable VARCHAR(50),
                    cuenta_iva_repercutido VARCHAR(50),
                    cuenta_deudas VARCHAR(50),
                    cuenta_cobros VARCHAR(50),
                    id_forma_pago INTEGER,
                    dia_pago1 INTEGER DEFAULT 0,
                    dia_pago2 INTEGER DEFAULT 0,
                    entidad_bancaria VARCHAR(4),
                    oficina_bancaria VARCHAR(4),
                    dc VARCHAR(2),
                    cuenta_corriente VARCHAR(10),
                    importe_a_cuenta DECIMAL(15,2) DEFAULT 0.00,
                    vales DECIMAL(15,2) DEFAULT 0.00,
                    visa_distancia1 VARCHAR(20),
                    visa_distancia2 VARCHAR(20),
                    visa1_caduca_mes INTEGER DEFAULT 0,
                    visa2_caduca_mes INTEGER DEFAULT 0,
                    visa1_caduca_ano INTEGER DEFAULT 0,
                    visa2_caduca_ano INTEGER DEFAULT 0,
                    visa1_cod_valid INTEGER DEFAULT 0,
                    visa2_cod_valid INTEGER DEFAULT 0,
                    acceso_web VARCHAR(100),
                    password_web VARCHAR(100),
                    id_tarifa INTEGER,
                    id_divisa INTEGER DEFAULT 1,
                    id_idioma_documentos INTEGER DEFAULT 1,
                    id_agente INTEGER,
                    id_transportista INTEGER
                )
            """
                )
            )

            # Tabla direcciones_alternativas (creada desde cero)
            conn.execute(
                text(
                    """
                CREATE TABLE IF NOT EXISTS direcciones_alternativas (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    id_cliente INTEGER NOT NULL,
                    descripcion VARCHAR(100),
                    direccion1 VARCHAR(255),
                    direccion2 VARCHAR(255),
                    cp VARCHAR(10),
                    poblacion VARCHAR(100),
                    provincia VARCHAR(100),
                    id_pais VARCHAR(100) DEFAULT 'España',
                    email VARCHAR(200),
                    telefono VARCHAR(50),
                    comentarios TEXT,
                    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                    fecha_modificacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_cliente) REFERENCES clientes(id)
                )
            """
                )
            )
            conn.commit()

        # Migrar datos desde la base de datos actual
        print("Migrating existing data...")

        with current_engine.connect() as source_conn, artstudio_engine.connect() as dest_conn:
            # Migrar tipos de cliente
            print("   Migrating customer type records...")
            try:
                result = source_conn.execute(text("SELECT * FROM tipocliente_def"))
                tipos = result.fetchall()
                for tipo in tipos:
                    dest_conn.execute(
                        text(
                            """
                        INSERT IGNORE INTO tipocliente_def
                        (id, nombre, `desc`)
                        VALUES (:id, :nombre, :desc)
                    """
                        ),
                        {"id": tipo[0], "nombre": tipo[1], "desc": tipo[2]},
                    )
                dest_conn.commit()
                print(f"      Migrados {len(tipos)} tipos de cliente")
            except Exception as e:
                print(f"      ⚠️  Error migrando tipos de cliente: {e}")

            # Migrar subtipos de cliente
            print("   Migrating customer subtype records...")
            try:
                result = source_conn.execute(text("SELECT * FROM tiposubcliente_def"))
                subtipos = result.fetchall()
                for subtipo in subtipos:
                    dest_conn.execute(
                        text(
                            """
                        INSERT IGNORE INTO tiposubcliente_def
                        (id, id_tipocliente, nombre, `desc`)
                        VALUES (:id, :id_tipocliente, :nombre, :desc)
                    """
                        ),
                        {
                            "id": subtipo[0],
                            "id_tipocliente": subtipo[1],
                            "nombre": subtipo[2],
                            "desc": subtipo[3],
                        },
                    )
                dest_conn.commit()
                print(f"      Migrados {len(subtipos)} subtipos de cliente")
            except Exception as e:
                print(f"      ⚠️  Error migrando subtipos de cliente: {e}")

            # Migrar clientes
            print("   Migrating customers...")
            try:
                result = source_conn.execute(text("SELECT * FROM clientes"))
                clientes = result.fetchall()
                for cliente in clientes:
                    # Asegurarse de que tenemos suficientes campos (rellenar con NULL si faltan)
                    cliente_data = list(cliente)
                    while len(cliente_data) < 55:  # Número aproximado de campos
                        cliente_data.append(None)

                    dest_conn.execute(
                        text(
                            """
                        INSERT IGNORE INTO clientes
                        (id, id_web, codigo_cliente, apellido1, apellido2, nombre, nombre_fiscal,
                         nombre_comercial, persona_contacto, cif_nif_siren, siret, cif_vies,
                         direccion1, direccion2, cp, poblacion, provincia, id_pais, telefono1,
                         telefono2, fax, movil, email, web, fecha_alta, fecha_ultima_compra,
                         fecha_nacimiento, acumulado_ventas, ventas_ejercicio, riesgo_maximo,
                         deuda_actual, importe_pendiente, comentarios, bloqueado, comentario_bloqueo,
                         observaciones, porc_dto_cliente, recargo_equivalencia, irpf, grupo_iva,
                         cuenta_contable, cuenta_iva_repercutido, cuenta_deudas, cuenta_cobros,
                         id_forma_pago, dia_pago1, dia_pago2, entidad_bancaria, oficina_bancaria,
                         dc, cuenta_corriente, importe_a_cuenta, vales, visa_distancia1,
                         visa_distancia2, visa1_caduca_mes, visa2_caduca_mes, visa1_caduca_ano,
                         visa2_caduca_ano, visa1_cod_valid, visa2_cod_valid, acceso_web,
                         password_web, id_tarifa, id_divisa, id_idioma_documentos, id_agente,
                         id_transportista)
                        VALUES (:id, :id_web, :codigo_cliente, :apellido1, :apellido2, :nombre,
                         :nombre_fiscal, :nombre_comercial, :persona_contacto, :cif_nif_siren,
                         :siret, :cif_vies, :direccion1, :direccion2, :cp, :poblacion, :provincia,
                         :id_pais, :telefono1, :telefono2, :fax, :movil, :email, :web, :fecha_alta,
                         :fecha_ultima_compra, :fecha_nacimiento, :acumulado_ventas, :ventas_ejercicio,
                         :riesgo_maximo, :deuda_actual, :importe_pendiente, :comentarios, :bloqueado,
                         :comentario_bloqueo, :observaciones, :porc_dto_cliente, :recargo_equivalencia,
                         :irpf, :grupo_iva, :cuenta_contable, :cuenta_iva_repercutido, :cuenta_deudas,
                         :cuenta_cobros, :id_forma_pago, :dia_pago1, :dia_pago2, :entidad_bancaria,
                         :oficina_bancaria, :dc, :cuenta_corriente, :importe_a_cuenta, :vales,
                         :visa_distancia1, :visa_distancia2, :visa1_caduca_mes, :visa2_caduca_mes,
                         :visa1_caduca_ano, :visa2_caduca_ano, :visa1_cod_valid, :visa2_cod_valid,
                         :acceso_web, :password_web, :id_tarifa, :id_divisa, :id_idioma_documentos,
                         :id_agente, :id_transportista)
                    """
                        ),
                        {
                            "id": cliente_data[0],
                            "id_web": cliente_data[1],
                            "codigo_cliente": cliente_data[2],
                            "apellido1": cliente_data[3],
                            "apellido2": cliente_data[4],
                            "nombre": cliente_data[5],
                            "nombre_fiscal": cliente_data[6],
                            "nombre_comercial": cliente_data[7],
                            "persona_contacto": cliente_data[8],
                            "cif_nif_siren": cliente_data[9],
                            "siret": cliente_data[10],
                            "cif_vies": cliente_data[11],
                            "direccion1": cliente_data[12],
                            "direccion2": cliente_data[13],
                            "cp": cliente_data[14],
                            "poblacion": cliente_data[15],
                            "provincia": cliente_data[16],
                            "id_pais": cliente_data[17],
                            "telefono1": cliente_data[18],
                            "telefono2": cliente_data[19],
                            "fax": cliente_data[20],
                            "movil": cliente_data[21],
                            "email": cliente_data[22],
                            "web": cliente_data[23],
                            "fecha_alta": cliente_data[24],
                            "fecha_ultima_compra": cliente_data[25],
                            "fecha_nacimiento": cliente_data[26],
                            "acumulado_ventas": cliente_data[27],
                            "ventas_ejercicio": cliente_data[28],
                            "riesgo_maximo": cliente_data[29],
                            "deuda_actual": cliente_data[30],
                            "importe_pendiente": cliente_data[31],
                            "comentarios": cliente_data[32],
                            "bloqueado": cliente_data[33],
                            "comentario_bloqueo": cliente_data[34],
                            "observaciones": cliente_data[35],
                            "porc_dto_cliente": cliente_data[36],
                            "recargo_equivalencia": cliente_data[37],
                            "irpf": cliente_data[38],
                            "grupo_iva": cliente_data[39],
                            "cuenta_contable": cliente_data[40],
                            "cuenta_iva_repercutido": cliente_data[41],
                            "cuenta_deudas": cliente_data[42],
                            "cuenta_cobros": cliente_data[43],
                            "id_forma_pago": cliente_data[44],
                            "dia_pago1": cliente_data[45],
                            "dia_pago2": cliente_data[46],
                            "entidad_bancaria": cliente_data[47],
                            "oficina_bancaria": cliente_data[48],
                            "dc": cliente_data[49],
                            "cuenta_corriente": cliente_data[50],
                            "importe_a_cuenta": cliente_data[51],
                            "vales": cliente_data[52],
                            "visa_distancia1": cliente_data[53],
                            "visa_distancia2": cliente_data[54],
                            "visa1_caduca_mes": (
                                cliente_data[55] if len(cliente_data) > 55 else 0
                            ),
                            "visa2_caduca_mes": (
                                cliente_data[56] if len(cliente_data) > 56 else 0
                            ),
                            "visa1_caduca_ano": (
                                cliente_data[57] if len(cliente_data) > 57 else 0
                            ),
                            "visa2_caduca_ano": (
                                cliente_data[58] if len(cliente_data) > 58 else 0
                            ),
                            "visa1_cod_valid": (
                                cliente_data[59] if len(cliente_data) > 59 else 0
                            ),
                            "visa2_cod_valid": (
                                cliente_data[60] if len(cliente_data) > 60 else 0
                            ),
                            "acceso_web": (
                                cliente_data[61] if len(cliente_data) > 61 else None
                            ),
                            "password_web": (
                                cliente_data[62] if len(cliente_data) > 62 else None
                            ),
                            "id_tarifa": (
                                cliente_data[63] if len(cliente_data) > 63 else None
                            ),
                            "id_divisa": (
                                cliente_data[64] if len(cliente_data) > 64 else 1
                            ),
                            "id_idioma_documentos": (
                                cliente_data[65] if len(cliente_data) > 65 else 1
                            ),
                            "id_agente": (
                                cliente_data[66] if len(cliente_data) > 66 else None
                            ),
                            "id_transportista": (
                                cliente_data[67] if len(cliente_data) > 67 else None
                            ),
                        },
                    )
                dest_conn.commit()
                print(f"      Migrados {len(clientes)} clientes")
            except Exception as e:
                print(f"      ⚠️  Error migrando clientes: {e}")

        print("✅ Migración completada exitosamente!")
        print("Summary:")
        print("   - Base de datos 'artstudio3d' creada")
        print(
            "   - Tablas específicas migradas: clientes, tipocliente_def, tiposubcliente_def, direcciones_alternativas"
        )
        print("   - Tabla direcciones_alternativas creada (vacía)")

    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        import traceback

        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    print("ArtStudio3D Database Creation Script")
    print("=" * 50)

    # Confirmar antes de proceder
    response = input(
        "⚠️  Esta operación creará una nueva base de datos 'artstudio3d' y migrará las tablas específicas. ¿Continuar? (y/N): "
    )
    if response.lower() != "y":
        print("❌ Operación cancelada")
        sys.exit(0)

    success = create_artstudio3d_database()
    if success:
        print("\nNext steps:")
        print(
            "1. Actualizar la configuración para usar 'artstudio3d' cuando sea necesario"
        )
        print("2. Probar la aplicación con las nuevas tablas")
        print("3. Poblar la tabla direcciones_alternativas según sea necesario")
    else:
        print("\n❌ La migración falló. Revisa los errores arriba.")
        sys.exit(1)
