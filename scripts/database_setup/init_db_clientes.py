"""
Script para inicializar la base de datos con datos de ejemplo
"""

from core.db import init_db, get_session
from modules.clientes.models import Cliente
from modules.clientes.repository import ClienteRepository
from datetime import date

def crear_clientes_demo():
    """Crea clientes de demostración"""
    session = get_session()
    repository = ClienteRepository(session)
    
    # Verificar si ya existen clientes
    clientes_existentes = repository.obtener_todos()
    if len(clientes_existentes) > 0:
        print(f"Ya existen {len(clientes_existentes)} clientes en la base de datos")
        return
    
    clientes_demo = [
        Cliente(
            codigo_cliente="C00001",
            nombre="Juan",
            apellido1="García",
            apellido2="Pérez",
            nombre_fiscal="García Pérez, Juan",
            cif_nif_siren="12345678A",
            direccion1="Calle Mayor, 123",
            cp="28001",
            poblacion="Madrid",
            provincia="Madrid",
            telefono1="666123456",
            email="juan@example.com",
            fecha_alta=date(2023, 1, 15)
        ),
        Cliente(
            codigo_cliente="C00002",
            nombre="María",
            apellido1="Martínez",
            apellido2="López",
            nombre_fiscal="Martínez López, María",
            nombre_comercial="Estudio Martínez",
            cif_nif_siren="87654321B",
            direccion1="Av. Diagonal, 456",
            cp="08008",
            poblacion="Barcelona",
            provincia="Barcelona",
            telefono1="666234567",
            movil="655234567",
            email="maria@estudiomartinez.com",
            web="www.estudiomartinez.com",
            fecha_alta=date(2023, 3, 20)
        ),
        Cliente(
            codigo_cliente="C00003",
            nombre="Pedro",
            apellido1="Fernández",
            apellido2="Ruiz",
            nombre_fiscal="Fernández Ruiz, Pedro",
            cif_nif_siren="11223344C",
            direccion1="Plaza España, 78",
            cp="46001",
            poblacion="Valencia",
            provincia="Valencia",
            telefono1="666345678",
            email="pedro@example.com",
            fecha_alta=date(2023, 5, 10)
        ),
        Cliente(
            codigo_cliente="C00004",
            nombre_fiscal="Creativos Unidos S.L.",
            nombre_comercial="Creativos Unidos",
            cif_nif_siren="B44332211",
            direccion1="Polígono Industrial, Nave 5",
            cp="41010",
            poblacion="Sevilla",
            provincia="Sevilla",
            telefono1="666456789",
            telefono2="954123456",
            email="info@creativosunidos.com",
            web="www.creativosunidos.com",
            fecha_alta=date(2023, 7, 5)
        ),
        Cliente(
            codigo_cliente="C00005",
            nombre="Carlos",
            apellido1="López",
            apellido2="Gómez",
            nombre_fiscal="López Gómez, Carlos",
            cif_nif_siren="55667788E",
            direccion1="Calle Real, 90",
            cp="48001",
            poblacion="Bilbao",
            provincia="Vizcaya",
            telefono1="666567890",
            email="carlos@example.com",
            fecha_alta=date(2023, 9, 15)
        ),
    ]
    
    print("Creando clientes de demostración...")
    for cliente in clientes_demo:
        repository.crear(cliente)
        print(f"  ✓ {cliente.nombre_fiscal}")
    
    print(f"\n✅ {len(clientes_demo)} clientes creados correctamente")
    session.close()


if __name__ == "__main__":
    print("Inicializando base de datos...")
    init_db()
    print("✓ Tablas creadas")
    
    print("\nCreando datos de ejemplo...")
    crear_clientes_demo()
    
    print("\n¡Listo! Se han agregado clientes a la tabla clientes.")
