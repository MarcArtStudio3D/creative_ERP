#!/usr/bin/env python3
"""
Script para migrar el campo id_pais a pais en todas las bases de datos reales
Incluye soporte para MariaDB, PostgreSQL y SQLite
"""

import os
import sqlite3

import psycopg2
import pymysql


def migrate_mariadb(host, port, user, password, database):
    """Migrar base de datos MariaDB/MySQL"""
    print(f"Migrating MariaDB: {database} on {host}:{port}")

    try:
        conn = pymysql.connect(
            host=host, port=port, user=user, password=password, database=database
        )
        cursor = conn.cursor()

        # Verificar tabla clientes
        cursor.execute("SHOW TABLES LIKE 'clientes'")
        if not cursor.fetchone():
            print("  ⚠️  No hay tabla clientes")
            return

        # Verificar estructura actual
        cursor.execute("DESCRIBE clientes")
        columns = cursor.fetchall()

        has_pais = any(col[0] == "pais" for col in columns)
        has_id_pais = any(col[0] == "id_pais" for col in columns)

        if has_pais and not has_id_pais:
            print("  ✅ Ya migrada")
            return
        elif not has_id_pais:
            print("  ❓ No tiene id_pais, estructura desconocida")
            return

        print("  Applying migration...")

        # Migrar tabla clientes
        if has_id_pais and not has_pais:
            cursor.execute("ALTER TABLE clientes ADD COLUMN pais VARCHAR(100)")
            cursor.execute(
                "UPDATE clientes SET pais = CASE id_pais WHEN 1 THEN 'España' WHEN 7 THEN 'Francia' ELSE 'España' END"
            )
            cursor.execute("ALTER TABLE clientes DROP COLUMN id_pais")
            print("    ✅ clientes migrada")

        # Migrar tabla direcciones_alternativas si existe
        cursor.execute("SHOW TABLES LIKE 'direcciones_alternativas'")
        if cursor.fetchone():
            cursor.execute("DESCRIBE direcciones_alternativas")
            alt_columns = cursor.fetchall()

            alt_has_pais = any(col[0] == "pais" for col in alt_columns)
            alt_has_id_pais = any(col[0] == "id_pais" for col in alt_columns)

            if alt_has_id_pais and not alt_has_pais:
                cursor.execute(
                    "ALTER TABLE direcciones_alternativas ADD COLUMN pais VARCHAR(100)"
                )
                cursor.execute(
                    "UPDATE direcciones_alternativas SET pais = CASE id_pais WHEN 1 THEN 'España' WHEN 7 THEN 'Francia' ELSE 'España' END"
                )
                cursor.execute(
                    "ALTER TABLE direcciones_alternativas DROP COLUMN id_pais"
                )
                print("    ✅ direcciones_alternativas migrada")

        conn.commit()
        cursor.close()
        conn.close()

        print("  ✅ Migración MariaDB completada")

    except Exception as e:
        print(f"  ❌ Error en MariaDB: {e}")


def migrate_postgresql(host, port, user, password, database):
    """Migrar base de datos PostgreSQL"""
    print(f"Migrating PostgreSQL: {database} on {host}:{port}")

    try:
        conn = psycopg2.connect(
            host=host, port=port, user=user, password=password, database=database
        )
        cursor = conn.cursor()

        # Verificar tabla clientes
        cursor.execute(
            "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'clientes')"
        )
        if not cursor.fetchone()[0]:
            print("  ⚠️  No hay tabla clientes")
            return

        # Verificar estructura actual
        cursor.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_name = 'clientes'"
        )
        columns = [row[0] for row in cursor.fetchall()]

        has_pais = "pais" in columns
        has_id_pais = "id_pais" in columns

        if has_pais and not has_id_pais:
            print("  ✅ Ya migrada")
            return
        elif not has_id_pais:
            print("  ❓ No tiene id_pais, estructura desconocida")
            return

        print("  Applying migration...")

        # Migrar tabla clientes
        if has_id_pais and not has_pais:
            cursor.execute("ALTER TABLE clientes ADD COLUMN pais VARCHAR(100)")
            cursor.execute(
                "UPDATE clientes SET pais = CASE id_pais WHEN 1 THEN 'España' WHEN 7 THEN 'Francia' ELSE 'España' END"
            )
            cursor.execute("ALTER TABLE clientes DROP COLUMN id_pais")
            print("    ✅ clientes migrada")

        # Migrar direcciones_alternativas si existe
        cursor.execute(
            "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'direcciones_alternativas')"
        )
        if cursor.fetchone()[0]:
            cursor.execute(
                "SELECT column_name FROM information_schema.columns WHERE table_name = 'direcciones_alternativas'"
            )
            alt_columns = [row[0] for row in cursor.fetchall()]

            alt_has_pais = "pais" in alt_columns
            alt_has_id_pais = "id_pais" in alt_columns

            if alt_has_id_pais and not alt_has_pais:
                cursor.execute(
                    "ALTER TABLE direcciones_alternativas ADD COLUMN pais VARCHAR(100)"
                )
                cursor.execute(
                    "UPDATE direcciones_alternativas SET pais = CASE id_pais WHEN 1 THEN 'España' WHEN 7 THEN 'Francia' ELSE 'España' END"
                )
                cursor.execute(
                    "ALTER TABLE direcciones_alternativas DROP COLUMN id_pais"
                )
                print("    ✅ direcciones_alternativas migrada")

        conn.commit()
        cursor.close()
        conn.close()

        print("  ✅ Migración PostgreSQL completada")

    except Exception as e:
        print(f"  ❌ Error en PostgreSQL: {e}")


def migrate_sqlite(db_path):
    """Migrar base de datos SQLite"""
    print(f"Migrating SQLite: {db_path}")

    if not os.path.exists(db_path):
        print(f"  ❌ Archivo no existe: {db_path}")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Verificar tabla clientes
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='clientes'"
        )
        if not cursor.fetchone():
            print("  ⚠️  No hay tabla clientes")
            return

        # Verificar estructura actual
        cursor.execute("PRAGMA table_info(clientes)")
        columns = [col[1] for col in cursor.fetchall()]

        has_pais = "pais" in columns
        has_id_pais = "id_pais" in columns

        if has_pais and not has_id_pais:
            print("  ✅ Ya migrada")
            return
        elif not has_id_pais:
            print("  ❓ No tiene id_pais, estructura desconocida")
            return

        print("  Applying migration...")

        # SQLite requiere recrear tabla para eliminar columna
        if has_id_pais and not has_pais:
            # Crear tabla temporal
            cursor.execute(
                """
                CREATE TABLE clientes_new AS 
                SELECT *, 
                       CASE id_pais 
                           WHEN 1 THEN 'España' 
                           WHEN 7 THEN 'Francia' 
                           ELSE 'España' 
                       END as pais
                FROM clientes
            """
            )

            # Eliminar columna id_pais de la nueva tabla
            cursor.execute("ALTER TABLE clientes_new DROP COLUMN id_pais")

            # Reemplazar tabla original
            cursor.execute("DROP TABLE clientes")
            cursor.execute("ALTER TABLE clientes_new RENAME TO clientes")

            print("    ✅ clientes migrada")

        # Migrar direcciones_alternativas si existe
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='direcciones_alternativas'"
        )
        if cursor.fetchone():
            cursor.execute("PRAGMA table_info(direcciones_alternativas)")
            alt_columns = [col[1] for col in cursor.fetchall()]

            alt_has_pais = "pais" in alt_columns
            alt_has_id_pais = "id_pais" in alt_columns

            if alt_has_id_pais and not alt_has_pais:
                cursor.execute(
                    """
                    CREATE TABLE direcciones_alternativas_new AS 
                    SELECT *, 
                           CASE id_pais 
                               WHEN 1 THEN 'España' 
                               WHEN 7 THEN 'Francia' 
                               ELSE 'España' 
                           END as pais
                    FROM direcciones_alternativas
                """
                )

                cursor.execute(
                    "ALTER TABLE direcciones_alternativas_new DROP COLUMN id_pais"
                )
                cursor.execute("DROP TABLE direcciones_alternativas")
                cursor.execute(
                    "ALTER TABLE direcciones_alternativas_new RENAME TO direcciones_alternativas"
                )

                print("    ✅ direcciones_alternativas migrada")

        conn.commit()
        cursor.close()
        conn.close()

        print("  ✅ Migración SQLite completada")

    except Exception as e:
        print(f"  ❌ Error en SQLite: {e}")


def migrate_empresas_table():
    """Migrar la tabla empresas en creative_erp_main"""
    print("Migrating empresas table into creative_erp_main...")

    try:
        conn = pymysql.connect(
            host="127.0.0.1",
            user="admin",
            password="admin123",
            database="creative_erp_main",
        )
        cursor = conn.cursor()

        # Verificar estructura
        cursor.execute("DESCRIBE empresas")
        columns = cursor.fetchall()

        has_pais = any(col[0] == "pais" for col in columns)
        has_id_pais = any(col[0] == "id_pais" for col in columns)

        if has_pais and not has_id_pais:
            print("  ✅ Tabla empresas ya migrada")
        elif has_id_pais and not has_pais:
            print("  Applying empresas table migration...")
            cursor.execute("ALTER TABLE empresas ADD COLUMN pais VARCHAR(100)")
            cursor.execute(
                "UPDATE empresas SET pais = CASE id_pais WHEN 1 THEN 'España' WHEN 7 THEN 'Francia' ELSE 'España' END"
            )
            cursor.execute("ALTER TABLE empresas DROP COLUMN id_pais")
            conn.commit()
            print("  ✅ Tabla empresas migrada")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"  ❌ Error migrando empresas: {e}")


def main():
    print("STARTING REAL DATABASE MIGRATION")
    print("=" * 50)

    # Primero migrar la tabla empresas
    migrate_empresas_table()

    # Obtener configuraciones de empresas
    try:
        conn = pymysql.connect(
            host="127.0.0.1",
            user="admin",
            password="admin123",
            database="creative_erp_main",
        )
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT 
                id, nombre_fiscal, motor_base_datos,
                nombre_base_datos_maria_db, host_mariadb, puerto_mariadb, usuario_mariadb, password_mariadb,
                nombre_base_datos_postgresql, host_postgresql, puerto_postgresql, usuario_postgresql, password_postgresql,
                ruta_base_datos_sqlite
            FROM empresas
        """
        )

        empresas = cursor.fetchall()

        for emp in empresas:
            print(f"\n--- EMPRESA {emp[0]}: {emp[1]} ---")

            if emp[2] == "MariaDB" and emp[3]:  # MariaDB
                migrate_mariadb(
                    host=emp[4] or "localhost",
                    port=emp[5] or 3306,
                    user=emp[6] or "admin",
                    password=emp[7] or "admin123",
                    database=emp[3],
                )

            elif emp[2] == "PostgreSQL" and emp[8]:  # PostgreSQL
                migrate_postgresql(
                    host=emp[9] or "localhost",
                    port=emp[10] or 5432,
                    user=emp[11] or "postgres",
                    password=emp[12] or "admin123",
                    database=emp[8],
                )

            elif emp[13]:  # SQLite
                migrate_sqlite(emp[13])

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Error obteniendo configuraciones: {e}")

    print("\nMIGRATION COMPLETED")
    print("=" * 50)


if __name__ == "__main__":
    main()
