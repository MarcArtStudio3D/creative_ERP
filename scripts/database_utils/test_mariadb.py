"""
Script de diagnóstico para verificar la conexión y estado de MariaDB
"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pymysql
from sqlalchemy import create_engine, text, inspect

MARIADB_URL = "mysql+pymysql://root:1234@127.0.0.1:3306/creative_erp"

print("=" * 60)
print("DIAGNÓSTICO DE CONEXIÓN MARIADB")
print("=" * 60)

# Test 1: Conexión directa con pymysql
print("\n1️⃣ Probando conexión directa con pymysql...")
try:
    conn = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="1234",
        database="creative_erp"
    )
    print("   ✅ Conexión exitosa con pymysql a la base de datos 'creative_erp'")
    
    cursor = conn.cursor()
    cursor.execute("SELECT VERSION();")
    version = cursor.fetchone()
    print(f"   📌 Versión MariaDB: {version[0]}")
    
    cursor.execute("SELECT DATABASE();")
    db = cursor.fetchone()
    print(f"   📌 Base de datos actual: {db[0]}")
    
    # Listar tablas en la base de datos actual
    print("\n   📋 Listando tablas en 'creative_erp':")
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    if tables:
        for table in tables:
            print(f"      - {table[0]}")
            # Contar registros en cada tabla
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]};")
            count = cursor.fetchone()
            print(f"        ({count[0]} registros)")
    else:
        print("      ⚠️  NO HAY TABLAS EN ESTA BASE DE DATOS")
    
    cursor.close()
    conn.close()
    
except pymysql.err.OperationalError as e:
    if e.args[0] == 1049:  # Unknown database error
        print(f"   ❌ La base de datos 'creative_erp' NO EXISTE")
        print(f"   💡 Necesitas crear la base de datos primero")
    else:
        print(f"   ❌ Error de conexión: {e}")
except Exception as e:
    print(f"   ❌ Error con pymysql: {e}")
    print(f"   Tipo de error: {type(e).__name__}")

# Test 2: Listar todas las bases de datos disponibles
print("\n2️⃣ Listando todas las bases de datos disponibles...")
try:
    conn = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="1234"
    )
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES;")
    databases = cursor.fetchall()
    print("   📋 Bases de datos encontradas:")
    for db in databases:
        print(f"      - {db[0]}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"   ❌ Error listando bases de datos: {e}")

# Test 3: Conexión con SQLAlchemy e inspección
print("\n3️⃣ Probando conexión con SQLAlchemy...")
try:
    engine = create_engine(MARIADB_URL)
    with engine.connect() as connection:
        result = connection.execute(text("SELECT DATABASE();"))
        db = result.fetchone()
        print(f"   ✅ Conexión exitosa con SQLAlchemy")
        print(f"   📌 Base de datos: {db[0]}")
        
        # Usar inspector para ver tablas
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"\n   📋 Tablas detectadas por SQLAlchemy ({len(tables)}):")
        if tables:
            for table in tables:
                print(f"      - {table}")
        else:
            print("      ⚠️  NO HAY TABLAS")
        
except Exception as e:
    print(f"   ❌ Error con SQLAlchemy: {e}")
    print(f"   Tipo de error: {type(e).__name__}")

# Test 4: Verificar modelos de SQLAlchemy
print("\n4️⃣ Verificando modelos de SQLAlchemy...")
try:
    from core.models import Base
    from modules.clientes.models import (
        Cliente, DireccionAlternativa, DeudaCliente, 
        HistorialCliente, EstadisticaClienteMes, Ville, ClienteTipo
    )
    
    print(f"   📌 Tablas definidas en Base.metadata ({len(Base.metadata.tables)}):")
    for table_name in Base.metadata.tables.keys():
        print(f"      - {table_name}")
    
except Exception as e:
    print(f"   ❌ Error cargando modelos: {e}")

print("\n" + "=" * 60)
print("FIN DEL DIAGNÓSTICO")
print("=" * 60)
