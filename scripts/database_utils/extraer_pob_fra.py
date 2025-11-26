# 1. Ruta del CSV original descargado
import csv
import pandas as pd
input_file = "communes-france-2025.csv"   # <-- cambia esto al nombre real

# 2. Intentar detectar el separador automáticamente y leer con pandas.
def detect_delimiter(path, sample_bytes=4096):
    with open(path, 'r', encoding='utf8', errors='ignore') as f:
        sample = f.read(sample_bytes)
    try:
        dialect = csv.Sniffer().sniff(sample)
        return dialect.delimiter
    except Exception:
        # default to comma
        return ','

sep = detect_delimiter(input_file)
print(f"Detected delimiter: {sep!r}")
df = pd.read_csv(input_file, sep=sep, dtype=str, engine='python', on_bad_lines='skip')

# 3. Seleccionar solo las columnas que necesitas
cols = ["code_postal","codes_postaux","code_insee",
         "nom_standard","nom_standard_majuscule",
         "reg_code","reg_nom","dep_code","dep_nom",
         "canton_code","canton_nom"]
missing = [c for c in cols if c not in df.columns]
if missing:
    print("Warning: these expected columns are missing in the CSV:", missing)
df_filtered = df[[c for c in cols if c in df.columns]]

# 4. Guardar resultado
output_file = "france_villes.csv"
df_filtered.to_csv(output_file, index=False, sep=";")

print("Archivo generado:", output_file)