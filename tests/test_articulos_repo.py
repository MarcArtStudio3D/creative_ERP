"""
Script de prueba para ArticuloRepository con SQL directo.
"""

import logging
logging.basicConfig(level=logging.DEBUG)

print("=" * 60)
print("PRUEBA DE ARTICULO REPOSITORY (SQL DIRECTO)")
print("=" * 60)

# 1. Inicializar MultiDBManager
print("\n1️⃣ Inicializando MultiDBManager...")
from core.db_manager import init_db_manager, get_db_manager

main_db_config = {
    'type': 'mariadb',
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'admin',
    'password': 'admin123',
    'database': 'creative_erp_main'
}

db_manager = init_db_manager(main_db_config)
print("✅ MultiDBManager inicializado")

# 2. Obtener empresa
print("\n2️⃣ Consultando empresa desde BD principal...")
empresa = db_manager.fetch_one(
    "SELECT * FROM empresas WHERE id = 1",
    use_main=True
)

if not empresa:
    print("❌ No se encontró empresa con ID 1")
    exit(1)

print(f"✅ Empresa: {empresa['nombre_fiscal']}")

# 3. Registrar y cambiar a empresa
print(f"\n3️⃣ Registrando empresa {empresa['id']}...")
db_config = {
    'type': 'mariadb',
    'host': empresa.get('host_mariadb', 'localhost'),
    'port': empresa.get('puerto_mariadb', 3306),
    'user': empresa.get('usuario_mariadb', 'admin'),
    'password': empresa.get('password_mariadb', 'admin123'),
    'database': empresa.get('nombre_base_datos_maria_db')
}

try:
    db_manager.register_empresa(empresa['id'], db_config)
    print(f"✅ Empresa {empresa['id']} registrada")
except Exception as e:
    print(f"⚠️ Empresa ya registrada o error: {e}")

db_manager.switch_empresa(empresa['id'])
print(f"✅ Cambiado a empresa {empresa['id']}")

# 4. Crear repository
print(f"\n4️⃣ Creando ArticuloRepository...")
from modules.articulos.repository_sql import ArticuloRepository

repo = ArticuloRepository()
print("✅ ArticuloRepository creado")

# 5. Obtener artículos
print(f"\n5️⃣ Obteniendo artículos (primeros 5)...")
articulos = repo.obtener_todos(limit=5)

print(f"✅ Encontrados {len(articulos)} artículos:")
for art in articulos:
    print(f"   - {art['codigo']}: {art['descripcion_reducida']} - Precio: {art.get('precio_venta', 0)}€")

# 6. Contar artículos
print(f"\n6️⃣ Contando total de artículos...")
total = repo.contar_todos()
print(f"✅ Total de artículos en BD: {total}")

# 7. Obtener un artículo por ID
if articulos:
    articulo_id = articulos[0]['id']
    print(f"\n7️⃣ Obteniendo artículo por ID {articulo_id}...")
    articulo = repo.obtener_por_id(articulo_id)

    if articulo:
        print(f"✅ Artículo encontrado:")
        print(f"   - Código: {articulo['codigo']}")
        print(f"   - Descripción: {articulo['descripcion_reducida']}")
        print(f"   - Precio venta: {articulo.get('precio_venta', 0)}€")
        print(f"   - Coste: {articulo.get('coste', 0)}€")
        print(f"   - Stock: {articulo.get('stock_real', 0)}")

        # 8. Obtener tarifas del artículo
        print(f"\n8️⃣ Obteniendo tarifas del artículo...")
        tarifas = repo.obtener_tarifas(articulo_id)

        if tarifas:
            print(f"✅ Encontradas {len(tarifas)} tarifas:")
            for tarifa in tarifas:
                print(f"   - {tarifa.get('codigo', 'N/A')}: {tarifa.get('precio', 0)}€ (dto: {tarifa.get('porc_dto', 0)}%)")
        else:
            print("⚠️ No hay tarifas para este artículo")

        # 9. Obtener promociones
        print(f"\n9️⃣ Obteniendo promociones del artículo...")
        promociones = repo.obtener_promociones(articulo_id)

        if promociones:
            print(f"✅ Encontradas {len(promociones)} promociones:")
            for promo in promociones:
                print(f"   - {promo.get('descripcion', 'N/A')}: {promo.get('precio_oferta', 0)}€")
        else:
            print("ℹ️ No hay promociones para este artículo")

# 10. Obtener secciones
print(f"\n🔟 Obteniendo secciones...")
secciones = repo.obtener_secciones()

if secciones:
    print(f"✅ Encontradas {len(secciones)} secciones:")
    for sec in secciones[:5]:  # Primeras 5
        print(f"   - {sec.get('codigo', 'N/A')}: {sec.get('seccion', 'N/A')}")
else:
    print("⚠️ No hay secciones en la BD")

# 11. Probar navegación (siguiente/anterior)
if articulos and len(articulos) > 1:
    articulo_id = articulos[0]['id']
    print(f"\n1️⃣1️⃣ Probando navegación desde artículo ID {articulo_id}...")

    siguiente = repo.obtener_siguiente(articulo_id)
    if siguiente:
        print(f"✅ Siguiente artículo: {siguiente['codigo']} - {siguiente['descripcion_reducida']}")
    else:
        print("ℹ️ No hay artículo siguiente")

    if len(articulos) > 1:
        articulo_id = articulos[1]['id']
        anterior = repo.obtener_anterior(articulo_id)
        if anterior:
            print(f"✅ Anterior artículo: {anterior['codigo']} - {anterior['descripcion_reducida']}")
        else:
            print("ℹ️ No hay artículo anterior")

print("\n" + "=" * 60)
print("✅ TODAS LAS PRUEBAS COMPLETADAS")
print("=" * 60)

# Cerrar conexiones
db_manager.close_all()
print("\n🔒 Conexiones cerradas")

