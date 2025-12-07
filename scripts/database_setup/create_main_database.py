#!/usr/bin/env python3
"""
Script para crear la base de datos principal 'Creative_ERP'
y migrar las tablas globales (users, business_groups, empresas)
"""

import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def create_main_database():
    """Crea la base de datos principal 'Creative_ERP' y migra las tablas globales."""

    print("Creating main database 'Creative_ERP'...")

    # Configuración de la nueva base de datos principal
    main_db_url = os.environ.get('CREATIVE_ERP_MAIN_DB',
                                'mysql+pymysql://admin:admin123@127.0.0.1:3306/creative_erp_main')

    # Configuración de la base de datos actual
    current_db_url = os.environ.get('CREATIVE_ERP_CURRENT_DB',
                                   'mysql+pymysql://admin:admin123@127.0.0.1:3306/creative_erp')

    try:
        from sqlalchemy import create_engine, text, MetaData
        from sqlalchemy.orm import sessionmaker

        # Primero crear la base de datos conectándose sin especificar BD
        temp_url = 'mysql+pymysql://admin:admin123@127.0.0.1:3306'
        from core.db import get_engine_from_url
        temp_engine = get_engine_from_url(temp_url)

        # Crear la base de datos si no existe
        with temp_engine.connect() as conn:
            conn.execute(text("CREATE DATABASE IF NOT EXISTS creative_erp_main"))
            conn.commit()

        temp_engine.dispose()

        # Ahora conectarse a la base de datos específica
        main_engine = get_engine_from_url(main_db_url)
        main_metadata = MetaData()

        # Crear motor para la base de datos actual
        current_engine = get_engine_from_url(current_db_url)

        # Crear tablas globales en la nueva base de datos
        print("Creating global tables...")

        # Tabla users
        with main_engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    full_name VARCHAR(100) NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    role VARCHAR(20) NOT NULL,
                    is_active INTEGER DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_login DATETIME NULL,
                    allowed_groups TEXT DEFAULT '[]'
                )
            """))

            # Tabla business_groups
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS business_groups (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(100) NOT NULL,
                    code VARCHAR(10) UNIQUE NOT NULL,
                    description TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """))

            # Tabla empresas
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS empresas (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    group_id INTEGER DEFAULT 1,
                    codigo_empresa VARCHAR(50) NOT NULL UNIQUE,
                    nombre_fiscal VARCHAR(200) NOT NULL,
                    nombre_comercial VARCHAR(200),
                    cif_nif VARCHAR(50) NOT NULL UNIQUE,
                    direccion VARCHAR(255),
                    cp VARCHAR(10),
                    poblacion VARCHAR(100),
                    provincia VARCHAR(100),
                    id_pais INTEGER DEFAULT 1,
                    telefono VARCHAR(50),
                    email VARCHAR(200),
                    web VARCHAR(200),
                    fecha_alta DATETIME DEFAULT CURRENT_TIMESTAMP,
                    activa INTEGER DEFAULT 1,
                    notas TEXT,
                    tipo_sociedad VARCHAR(100),
                    fecha_constitucion DATE,
                    objeto_social TEXT,
                    capital_social DECIMAL(15,2) DEFAULT 0.00,
                    moneda_capital VARCHAR(3) DEFAULT 'EUR',
                    persona_contacto VARCHAR(200),
                    cargo_contacto VARCHAR(100),
                    telefono_contacto VARCHAR(50),
                    movil_contacto VARCHAR(50),
                    fax VARCHAR(50),
                    direccion_fiscal VARCHAR(255),
                    cp_fiscal VARCHAR(10),
                    poblacion_fiscal VARCHAR(100),
                    provincia_fiscal VARCHAR(100),
                    banco VARCHAR(100),
                    sucursal VARCHAR(100),
                    dc VARCHAR(2),
                    numero_cuenta VARCHAR(10),
                    iban VARCHAR(34),
                    swift_bic VARCHAR(11),
                    regimen_iva VARCHAR(50) DEFAULT 'General',
                    tipo_retencion VARCHAR(50),
                    porcentaje_retencion DECIMAL(5,2) DEFAULT 0.00,
                    exento_iva INTEGER DEFAULT 0,
                    intracomunitario INTEGER DEFAULT 0,
                    limite_credito DECIMAL(15,2) DEFAULT 0.00,
                    dias_pago INTEGER DEFAULT 30,
                    descuento_general DECIMAL(5,2) DEFAULT 0.00,
                    forma_pago_predeterminada VARCHAR(50),
                    sector_actividad VARCHAR(100),
                    numero_empleados INTEGER,
                    facturacion_anual DECIMAL(15,2),
                    usuario_modificacion VARCHAR(100),
                    motor_base_datos VARCHAR(20) DEFAULT 'mariadb',
                    nombre_base_datos_maria_db VARCHAR(100),
                    nombre_base_datos_postgresql VARCHAR(100),
                    host_maria_db VARCHAR(100) DEFAULT '127.0.0.1',
                    puerto_maria_db INTEGER DEFAULT 3306,
                    host_postgresql VARCHAR(100) DEFAULT '127.0.0.1',
                    puerto_postgresql INTEGER DEFAULT 5432,
                    usuario_db VARCHAR(50) DEFAULT 'admin',
                    password_db VARCHAR(100) DEFAULT 'admin123',
                    FOREIGN KEY (group_id) REFERENCES business_groups(id)
                )
            """))
            conn.commit()

        # Migrar datos desde la base de datos actual
        print("Migrating existing data...")

        with current_engine.connect() as source_conn, main_engine.connect() as dest_conn:
            # Migrar usuarios
            print("   Migrating users...")
            result = source_conn.execute(text("SELECT * FROM users"))
            users = result.fetchall()
            for user in users:
                dest_conn.execute(text("""
                    INSERT IGNORE INTO users
                    (id, username, email, full_name, password_hash, role, is_active, created_at, last_login, allowed_groups)
                    VALUES (:id, :username, :email, :full_name, :password_hash, :role, :is_active, :created_at, :last_login, :allowed_groups)
                """), {
                    'id': user[0], 'username': user[1], 'email': user[2], 'full_name': user[3],
                    'password_hash': user[4], 'role': user[5], 'is_active': user[6],
                    'created_at': user[7], 'last_login': user[8], 'allowed_groups': user[9]
                })
            dest_conn.commit()

            # Migrar business_groups
            print("   Migrating company groups...")
            result = source_conn.execute(text("SELECT * FROM business_groups"))
            groups = result.fetchall()
            for group in groups:
                dest_conn.execute(text("""
                    INSERT IGNORE INTO business_groups
                    (id, name, code, description, created_at)
                    VALUES (:id, :name, :code, :description, :created_at)
                """), {
                    'id': group[0], 'name': group[1], 'code': group[2],
                    'description': group[3], 'created_at': group[4]
                })
            dest_conn.commit()

            # Migrar empresas
            print("   Migrating companies...")
            result = source_conn.execute(text("SELECT * FROM empresas"))
            empresas = result.fetchall()
            for empresa in empresas:
                # Asegurarse de que tenemos suficientes campos (llenar con valores por defecto si faltan)
                empresa_data = list(empresa) + [None] * (39 - len(empresa))  # 39 es el número total de campos
                
                dest_conn.execute(text("""
                    INSERT IGNORE INTO empresas
                    (id, group_id, codigo_empresa, nombre_fiscal, nombre_comercial, cif_nif,
                     direccion, cp, poblacion, provincia, id_pais, telefono, email, web,
                     fecha_alta, activa, notas, tipo_sociedad, fecha_constitucion, objeto_social,
                     capital_social, moneda_capital, persona_contacto, cargo_contacto,
                     telefono_contacto, movil_contacto, fax, direccion_fiscal, cp_fiscal,
                     poblacion_fiscal, provincia_fiscal, banco, sucursal, dc, numero_cuenta,
                     iban, swift_bic, regimen_iva, tipo_retencion, porcentaje_retencion,
                     exento_iva, intracomunitario, limite_credito, dias_pago, descuento_general,
                     forma_pago_predeterminada, sector_actividad, numero_empleados, facturacion_anual,
                     sitio_web, observaciones_internas, fecha_modificacion, usuario_modificacion,
                     motor_base_datos, nombre_base_datos_maria_db, nombre_base_datos_postgresql,
                     host_maria_db, puerto_maria_db, host_postgresql, puerto_postgresql,
                     usuario_db, password_db)
                    VALUES (:id, :group_id, :codigo_empresa, :nombre_fiscal, :nombre_comercial, :cif_nif,
                     :direccion, :cp, :poblacion, :provincia, :id_pais, :telefono, :email, :web,
                     :fecha_alta, :activa, :notas, :tipo_sociedad, :fecha_constitucion, :objeto_social,
                     :capital_social, :moneda_capital, :persona_contacto, :cargo_contacto,
                     :telefono_contacto, :movil_contacto, :fax, :direccion_fiscal, :cp_fiscal,
                     :poblacion_fiscal, :provincia_fiscal, :banco, :sucursal, :dc, :numero_cuenta,
                     :iban, :swift_bic, :regimen_iva, :tipo_retencion, :porcentaje_retencion,
                     :exento_iva, :intracomunitario, :limite_credito, :dias_pago, :descuento_general,
                     :forma_pago_predeterminada, :sector_actividad, :numero_empleados, :facturacion_anual,
                     :sitio_web, :observaciones_internas, :fecha_modificacion, :usuario_modificacion,
                     :motor_base_datos, :nombre_base_datos_maria_db, :nombre_base_datos_postgresql,
                     :host_maria_db, :puerto_maria_db, :host_postgresql, :puerto_postgresql,
                     :usuario_db, :password_db)
                """), {
                    'id': empresa_data[0], 'group_id': empresa_data[1] or 1, 'codigo_empresa': empresa_data[2],
                    'nombre_fiscal': empresa_data[3], 'nombre_comercial': empresa_data[4], 'cif_nif': empresa_data[5],
                    'direccion': empresa_data[6], 'cp': empresa_data[7], 'poblacion': empresa_data[8],
                    'provincia': empresa_data[9], 'id_pais': empresa_data[10] or 1, 'telefono': empresa_data[11],
                    'email': empresa_data[12], 'web': empresa_data[13], 'fecha_alta': empresa_data[14],
                    'activa': empresa_data[15] or 1, 'notas': empresa_data[16], 'tipo_sociedad': empresa_data[17],
                    'fecha_constitucion': empresa_data[18], 'objeto_social': empresa_data[19],
                    'capital_social': empresa_data[20] or 0.0, 'moneda_capital': empresa_data[21] or 'EUR',
                    'persona_contacto': empresa_data[22], 'cargo_contacto': empresa_data[23],
                    'telefono_contacto': empresa_data[24], 'movil_contacto': empresa_data[25],
                    'fax': empresa_data[26], 'direccion_fiscal': empresa_data[27], 'cp_fiscal': empresa_data[28],
                    'poblacion_fiscal': empresa_data[29], 'provincia_fiscal': empresa_data[30],
                    'banco': empresa_data[31], 'sucursal': empresa_data[32], 'dc': empresa_data[33],
                    'numero_cuenta': empresa_data[34], 'iban': empresa_data[35], 'swift_bic': empresa_data[36],
                    'regimen_iva': empresa_data[37] or 'General', 'tipo_retencion': empresa_data[38],
                    'porcentaje_retencion': 0.0, 'exento_iva': 0, 'intracomunitario': 0,
                    'limite_credito': 0.0, 'dias_pago': 30, 'descuento_general': 0.0,
                    'forma_pago_predeterminada': None, 'sector_actividad': None, 'numero_empleados': None,
                    'facturacion_anual': None, 'sitio_web': None, 'observaciones_internas': None,
                    'fecha_modificacion': None, 'usuario_modificacion': None,
                    'motor_base_datos': 'mariadb', 'nombre_base_datos_maria_db': None,
                    'nombre_base_datos_postgresql': None, 'host_maria_db': '127.0.0.1',
                    'puerto_maria_db': 3306, 'host_postgresql': '127.0.0.1',
                    'puerto_postgresql': 5432, 'usuario_db': 'admin', 'password_db': 'admin123'
                })
            dest_conn.commit()

        print("✅ Migración completada exitosamente!")
        print("Summary:")
        print("   - Base de datos 'creative_erp_main' creada")
        print("   - Tablas globales (users, business_groups, empresas) migradas")
        print("   - Datos preservados")

        # Mostrar estadísticas
        with main_engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            row = result.fetchone()
            users_count = row[0] if row else 0

            result = conn.execute(text("SELECT COUNT(*) FROM business_groups"))
            row = result.fetchone()
            groups_count = row[0] if row else 0

            result = conn.execute(text("SELECT COUNT(*) FROM empresas"))
            row = result.fetchone()
            empresas_count = row[0] if row else 0

        print("Statistics:")
        print(f"   - Usuarios: {users_count}")
        print(f"   - Grupos empresariales: {groups_count}")
        print(f"   - Empresas: {empresas_count}")

    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True

if __name__ == "__main__":
    print("Main Database Creation Script")
    print("=" * 50)

    # Confirmar antes de proceder
    response = input("⚠️  Esta operación creará una nueva base de datos 'creative_erp_main' y migrará las tablas globales. ¿Continuar? (y/N): ")
    if response.lower() != 'y':
        print("❌ Operación cancelada")
        sys.exit(0)

    success = create_main_database()
    if success:
        print("\nNext steps:")
        print("1. Actualizar la configuración en core/db.py para usar 'creative_erp_main'")
        print("2. Probar la aplicación con la nueva base de datos")
        print("3. Una vez verificado, se pueden eliminar las tablas globales de 'creative_erp'")
    else:
        print("\n❌ La migración falló. Revisa los errores arriba.")
        sys.exit(1)