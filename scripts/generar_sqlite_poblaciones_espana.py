import os
import sqlite3
import tempfile
import csv
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# URLs de los CSV en GitHub
URL_CP = "https://raw.githubusercontent.com/inigoflores/ds-codigos-postales-ine-es/master/data/codigos_postales_municipios.csv"  # CP → municipio_id :contentReference[oaicite:2]{index=2}  
URL_MUNICIPIOS = "https://raw.githubusercontent.com/codeforspain/ds-organizacion-administrativa/master/data/municipios.csv"  # municipio_id → provincia_id, nombre municipio :contentReference[oaicite:3]{index=3}  
URL_PROVINCIAS = "https://raw.githubusercontent.com/codeforspain/ds-organizacion-administrativa/master/data/provincias.csv"  # provincia_id → nombre provincia :contentReference[oaicite:4]{index=4}  

DB_PATH = "cp_poblacion_provincia.sqlite"
TABLE_NAME = "cp_info"

def descargar_csv(url):
    print(f"Descargando {url} …")
    req = Request(url, headers={"User-Agent": "python-urllib"})
    try:
        with urlopen(req, timeout=60) as resp:
            data = resp.read().decode("utf-8")
    except HTTPError as e:
        raise RuntimeError(f"HTTP Error {e.code} al descargar {url}")
    except URLError as e:
        raise RuntimeError(f"URL Error {e} al descargar {url}")
    # Guardamos en un fichero temporal
    fd, tmpfile = tempfile.mkstemp(suffix=".csv")
    os.close(fd)
    with open(tmpfile, "w", encoding="utf-8") as f:
        f.write(data)
    print("Guardado en:", tmpfile)
    return tmpfile

def cargar_provincias(csv_prov):
    """Lee el CSV de provincias y devuelve dict provincia_id → nombre_provincia."""
    d = {}
    with open(csv_prov, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        # Revisar los nombres exactos de columna
        for row in reader:
            pid = row.get("provincia_id") or row.get("id") or row.get("codigo")
            nombre = row.get("nombre") or row.get("provincia_nombre")
            if pid is not None and nombre is not None:
                d[pid] = nombre
    return d

def cargar_municipios(csv_mun, provincias_map):
    """
    Lee el CSV de municipios.
    Devuelve dict municipio_id → (nombre_municipio, nombre_provincia)
    """
    d = {}
    with open(csv_mun, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mid = row.get("municipio_id")
            nombre_mun = row.get("nombre")
            pid = row.get("provincia_id")
            if mid is None:
                continue
            nombre_prov = provincias_map.get(pid, None)
            d[mid] = (nombre_mun, nombre_prov)
    return d

def importar_a_sqlite(csv_cp, municipios_map, sqlite_path):
    conn = sqlite3.connect(sqlite_path)
    cur = conn.cursor()

    # Crear tabla
    cur.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")
    cur.execute(f"""
        CREATE TABLE {TABLE_NAME} (
            cp TEXT,
            poblacion TEXT,
            provincia TEXT
        )
    """)
    conn.commit()

    # Leer CP y cruzar
    with open(csv_cp, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        inserted = 0
        for row in reader:
            cp = row.get("codigo_postal") or row.get("postal_code")
            mid = row.get("municipio_id")
            if mid is None:
                continue
            poblacion, provincia = municipios_map.get(mid, (None, None))
            if poblacion is None:
                # si no está en el mapeo, usar el valor del CSV de CP si existe el nombre
                poblacion = row.get("municipio_nombre", "")
            # Insertar
            cur.execute(f"INSERT INTO {TABLE_NAME} (cp, poblacion, provincia) VALUES (?, ?, ?)",
                        (cp, poblacion, provincia))
            inserted += 1

    conn.commit()
    conn.close()
    print(f"Insertadas {inserted} filas en la base de datos {sqlite_path}")

def main():
    tmp_cp = descargar_csv(URL_CP)
    tmp_mun = descargar_csv(URL_MUNICIPIOS)
    tmp_prov = descargar_csv(URL_PROVINCIAS)

    provincias_map = cargar_provincias(tmp_prov)
    municipios_map = cargar_municipios(tmp_mun, provincias_map)

    importar_a_sqlite(tmp_cp, municipios_map, DB_PATH)

    # limpiar archivos temporales
    os.remove(tmp_cp)
    os.remove(tmp_mun)
    os.remove(tmp_prov)
    print("SQLite generado:", DB_PATH)

if __name__ == "__main__":
    main()
