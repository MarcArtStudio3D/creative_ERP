import sqlite3
import pandas as pd
import os

# ----------------------------------------
# CONFIGURACIÓN
# ----------------------------------------

CSV_FILE = "france_villes.csv"     # <-- tu CSV ya filtrado
DB_FILE = "france.db"             # Nombre de la base de datos SQLite
TABLE_NAME = "villes"           # Nombre de la tabla


# ----------------------------------------
# FUNCIÓN PRINCIPAL
# ----------------------------------------

def csv_to_sqlite(csv_file, db_file, table_name):
    # Cargar CSV (data.gouv suele usar ';')
    df = pd.read_csv(csv_file, sep=";", dtype=str)

    # Si existe una DB antigua, eliminarla
    if os.path.exists(db_file):
        os.remove(db_file)

    # Conexión a SQLite
    conn = sqlite3.connect(db_file)

    # Exportar el DataFrame completo a SQLite
    df.to_sql(table_name, conn, if_exists="replace", index=False)

    conn.close()

    print(f"✓ Base SQLite creada: {db_file}")
    print(f"✓ Tabla: {table_name}")
    print(f"✓ Columnas importadas: {list(df.columns)}")
    print(f"✓ Registros insertados: {len(df)}")


# ----------------------------------------
# EJECUCIÓN
# ----------------------------------------

if __name__ == "__main__":
    csv_to_sqlite(CSV_FILE, DB_FILE, TABLE_NAME)
