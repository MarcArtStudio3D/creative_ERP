"""
Repositorio para el módulo de Clientes
Maneja todas las operaciones CRUD y lógica de negocio
"""

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, extract, func
from datetime import date, datetime
from typing import List, Optional, Dict
from modules.clientes.models import (
    Cliente, DireccionAlternativa, DeudaCliente, 
    HistorialCliente, EstadisticaClienteMes, ClienteTipo
)


class ClienteRepository:
    """Repositorio para operaciones con clientes"""
    
    def __init__(self, session: Session):
        self.session = session
    
    # ========== CRUD Básico ==========
    
    def obtener_todos(self, filtro: str = "") -> List[Cliente]:
        """Obtiene todos los clientes, opcionalmente filtrados"""
        query = self.session.query(Cliente)
        
        if filtro:
            filtro_like = f"%{filtro}%"
            query = query.filter(
                or_(
                    Cliente.codigo_cliente.ilike(filtro_like),
                    Cliente.nombre_fiscal.ilike(filtro_like),
                    Cliente.nombre_comercial.ilike(filtro_like),
                    Cliente.cif_nif_siren.ilike(filtro_like),
                    Cliente.email.ilike(filtro_like)
                )
            )
        
        return query.order_by(Cliente.nombre_fiscal).all()
    
    def obtener_por_id(self, id_cliente: int) -> Optional[Cliente]:
        """Obtiene un cliente por su ID"""
        return self.session.query(Cliente).filter(Cliente.id == id_cliente).first()
    
    def obtener_por_codigo(self, codigo: str) -> Optional[Cliente]:
        """Obtiene un cliente por su código"""
        return self.session.query(Cliente).filter(Cliente.codigo_cliente == codigo).first()
    
    def obtener_por_cif(self, cif: str) -> Optional[Cliente]:
        """Obtiene un cliente por su CIF/NIF"""
        return self.session.query(Cliente).filter(Cliente.cif_nif_siren == cif).first()
    
    def crear(self, cliente: Cliente) -> Cliente:
        """Crea un nuevo cliente"""
        # Generar código automático si no existe
        if not cliente.codigo_cliente:
            cliente.codigo_cliente = self._generar_codigo()
        
        # Inicializar cuentas contables predeterminadas si no existen
        if not cliente.cuenta_contable:
            cliente.cuenta_contable = f"430{cliente.codigo_cliente}"
        
        self.session.add(cliente)
        self.session.commit()
        self.session.refresh(cliente)
        
        # Registrar en historial
        self._registrar_historial(
            cliente.id,
            "alta",
            "Cliente dado de alta",
            0.0
        )
        
        return cliente
    
    def actualizar(self, cliente: Cliente) -> Cliente:
        """Actualiza un cliente existente"""
        self.session.commit()
        self.session.refresh(cliente)
        
        # Registrar en historial
        self._registrar_historial(
            cliente.id,
            "modificacion",
            "Datos del cliente modificados",
            0.0
        )
        
        return cliente
    
    def eliminar(self, id_cliente: int) -> bool:
        """Elimina un cliente (soft delete o verificación de dependencias)"""
        cliente = self.obtener_por_id(id_cliente)
        if not cliente:
            return False
        
        # Verificar si tiene facturas/documentos pendientes
        tiene_deudas = self.session.query(DeudaCliente).filter(
            and_(
                DeudaCliente.id_cliente == id_cliente,
                DeudaCliente.pagado == False
            )
        ).count() > 0
        
        if tiene_deudas:
            raise ValueError("No se puede eliminar un cliente con deudas pendientes")
        
        # Eliminar registros relacionados
        self.session.query(DireccionAlternativa).filter(
            DireccionAlternativa.id_cliente == id_cliente
        ).delete()
        
        self.session.query(DeudaCliente).filter(
            DeudaCliente.id_cliente == id_cliente
        ).delete()
        
        self.session.query(HistorialCliente).filter(
            HistorialCliente.id_cliente == id_cliente
        ).delete()
        
        self.session.query(EstadisticaClienteMes).filter(
            EstadisticaClienteMes.id_cliente == id_cliente
        ).delete()
        
        # Eliminar cliente
        self.session.delete(cliente)
        self.session.commit()
        
        return True
    
    # ========== Direcciones Alternativas ==========
    
    def obtener_direcciones(self, id_cliente: int) -> List[DireccionAlternativa]:
        """Obtiene todas las direcciones alternativas de un cliente"""
        return self.session.query(DireccionAlternativa).filter(
            DireccionAlternativa.id_cliente == id_cliente
        ).all()
    
    def obtener_direccion_por_id(self, id_direccion: int) -> Optional[DireccionAlternativa]:
        """Obtiene una dirección alternativa por su ID"""
        return self.session.query(DireccionAlternativa).filter(
            DireccionAlternativa.id == id_direccion
        ).first()
    
    def crear_direccion(self, direccion: DireccionAlternativa) -> DireccionAlternativa:
        """Crea una nueva dirección alternativa"""
        self.session.add(direccion)
        self.session.commit()
        self.session.refresh(direccion)
        return direccion
    
    def guardar_direccion(self, direccion: DireccionAlternativa) -> DireccionAlternativa:
        """Guarda (crea o actualiza) una dirección alternativa"""
        if direccion.id:
            # Es una actualización
            self.session.merge(direccion)
        else:
            # Es nueva
            self.session.add(direccion)
        self.session.commit()
        self.session.refresh(direccion)
        return direccion
    
    def eliminar_direccion(self, id_direccion: int) -> bool:
        """Elimina una dirección alternativa"""
        direccion = self.session.query(DireccionAlternativa).filter(
            DireccionAlternativa.id == id_direccion
        ).first()
        
        if direccion:
            self.session.delete(direccion)
            self.session.commit()
            return True
        return False
    
    # ========== Gestión de Deudas ==========
    
    def obtener_deudas(self, id_cliente: int, solo_pendientes: bool = True) -> List[DeudaCliente]:
        """Obtiene las deudas de un cliente"""
        query = self.session.query(DeudaCliente).filter(
            DeudaCliente.id_cliente == id_cliente
        )
        
        if solo_pendientes:
            query = query.filter(DeudaCliente.pagado == False)
        
        return query.order_by(DeudaCliente.fecha_vencimiento).all()
    
    def registrar_deuda(self, deuda: DeudaCliente) -> DeudaCliente:
        """Registra una nueva deuda"""
        self.session.add(deuda)
        
        # Actualizar deuda actual del cliente
        cliente = self.obtener_por_id(deuda.id_cliente)
        if cliente:
            cliente.deuda_actual += deuda.importe_pendiente
        
        self.session.commit()
        self.session.refresh(deuda)
        return deuda
    
    def registrar_pago(self, id_deuda: int, importe_pagado: float, fecha_pago: date = None) -> bool:
        """Registra un pago parcial o total de una deuda"""
        deuda = self.session.query(DeudaCliente).filter(
            DeudaCliente.id == id_deuda
        ).first()
        
        if not deuda:
            return False
        
        deuda.importe_pagado += importe_pagado
        deuda.importe_pendiente = deuda.importe_total - deuda.importe_pagado
        
        if deuda.importe_pendiente <= 0:
            deuda.pagado = True
            deuda.fecha_pago = fecha_pago or date.today()
        
        # Actualizar deuda actual del cliente
        cliente = self.obtener_por_id(deuda.id_cliente)
        if cliente:
            cliente.deuda_actual -= importe_pagado
            if cliente.deuda_actual < 0:
                cliente.deuda_actual = 0
        
        # Registrar en historial
        self._registrar_historial(
            deuda.id_cliente,
            "cobro",
            f"Cobro de {importe_pagado}€ - Doc: {deuda.documento}",
            importe_pagado
        )
        
        self.session.commit()
        return True
    
    def calcular_deuda_total(self, id_cliente: int) -> float:
        """Calcula la deuda total pendiente de un cliente"""
        total = self.session.query(func.sum(DeudaCliente.importe_pendiente)).filter(
            and_(
                DeudaCliente.id_cliente == id_cliente,
                DeudaCliente.pagado == False
            )
        ).scalar()
        
        return total or 0.0
    
    # ========== Estadísticas ==========
    
    def obtener_estadisticas_mes(self, id_cliente: int, anio: int) -> Dict[int, float]:
        """Obtiene las estadísticas de ventas por mes para un año"""
        stats = self.session.query(EstadisticaClienteMes).filter(
            and_(
                EstadisticaClienteMes.id_cliente == id_cliente,
                EstadisticaClienteMes.anio == anio
            )
        ).all()
        
        # Crear diccionario con todos los meses (inicializados a 0)
        resultado = {mes: 0.0 for mes in range(1, 13)}
        
        # Rellenar con los datos reales
        for stat in stats:
            resultado[stat.mes] = stat.importe_ventas
        
        return resultado
    
    def actualizar_estadistica(self, id_cliente: int, fecha: date, importe: float):
        """Actualiza las estadísticas de un cliente tras una venta"""
        anio = fecha.year
        mes = fecha.month
        
        # Buscar registro existente
        stat = self.session.query(EstadisticaClienteMes).filter(
            and_(
                EstadisticaClienteMes.id_cliente == id_cliente,
                EstadisticaClienteMes.anio == anio,
                EstadisticaClienteMes.mes == mes
            )
        ).first()
        
        if stat:
            stat.importe_ventas += importe
            stat.numero_operaciones += 1
        else:
            stat = EstadisticaClienteMes(
                id_cliente=id_cliente,
                anio=anio,
                mes=mes,
                importe_ventas=importe,
                numero_operaciones=1
            )
            self.session.add(stat)
        
        # Actualizar campos del cliente
        cliente = self.obtener_por_id(id_cliente)
        if cliente:
            cliente.acumulado_ventas += importe
            cliente.ventas_ejercicio += importe
            cliente.fecha_ultima_compra = fecha
        
        self.session.commit()
    
    # ========== Historial ==========
    
    def obtener_historial(self, id_cliente: int, limite: int = 100) -> List[HistorialCliente]:
        """Obtiene el historial de operaciones de un cliente"""
        return self.session.query(HistorialCliente).filter(
            HistorialCliente.id_cliente == id_cliente
        ).order_by(HistorialCliente.fecha.desc()).limit(limite).all()
    
    def _registrar_historial(self, id_cliente: int, tipo: str, descripcion: str, importe: float = 0.0):
        """Registra una entrada en el historial del cliente"""
        historial = HistorialCliente(
            id_cliente=id_cliente,
            fecha=date.today(),
            tipo_operacion=tipo,
            descripcion=descripcion,
            importe=importe,
            usuario="sistema"  # TODO: Obtener usuario actual
        )
        self.session.add(historial)
    
    # ========== Utilidades ==========
    
    def _generar_codigo(self) -> str:
        """Genera un código automático para un nuevo cliente"""
        # Obtener el último código numérico
        ultimo = self.session.query(Cliente).order_by(Cliente.id.desc()).first()
        
        if ultimo and ultimo.codigo_cliente:
            # Intentar extraer número del código
            try:
                numero = int(ultimo.codigo_cliente.replace("C", ""))
                return f"C{numero + 1:05d}"
            except ValueError:
                pass
        
        # Código por defecto
        return f"C{1:05d}"
    
    def buscar(self, termino: str) -> List[Cliente]:
        """Búsqueda avanzada de clientes"""
        return self.obtener_todos(filtro=termino)
    
    def obtener_con_deudas_vencidas(self) -> List[Cliente]:
        """Obtiene clientes con deudas vencidas"""
        hoy = date.today()
        
        subquery = self.session.query(DeudaCliente.id_cliente).filter(
            and_(
                DeudaCliente.pagado == False,
                DeudaCliente.fecha_vencimiento < hoy
            )
        ).distinct()
        
        return self.session.query(Cliente).filter(
            Cliente.id.in_(subquery)
        ).all()
    
    def obtener_bloqueados(self) -> List[Cliente]:
        """Obtiene clientes bloqueados"""
        return self.session.query(Cliente).filter(
            Cliente.bloqueado == True
        ).all()

    # ========== Tipos de Cliente ==========

    def obtener_tipos_cliente(self, id_cliente: int) -> List[ClienteTipo]:
        """Obtiene los tipos asociados a un cliente"""
        return self.session.query(ClienteTipo)\
            .options(joinedload(ClienteTipo.tipo), joinedload(ClienteTipo.subtipo))\
            .filter(ClienteTipo.id_cliente == id_cliente)\
            .all()

    def agregar_tipo_cliente(self, id_cliente: int, id_tipo: int, id_subtipo: Optional[int] = None) -> ClienteTipo:
        """Asocia un tipo a un cliente"""
        # Verificar si ya existe
        query = self.session.query(ClienteTipo).filter(
            ClienteTipo.id_cliente == id_cliente,
            ClienteTipo.id_tipo == id_tipo
        )
        if id_subtipo:
            query = query.filter(ClienteTipo.id_subtipo == id_subtipo)
        else:
            query = query.filter(ClienteTipo.id_subtipo.is_(None))
            
        exists = query.first()
        if exists:
            return exists
            
        nuevo = ClienteTipo(
            id_cliente=id_cliente,
            id_tipo=id_tipo,
            id_subtipo=id_subtipo
        )
        self.session.add(nuevo)
        self.session.commit()
        return nuevo

    def eliminar_tipo_cliente(self, id_asociacion: int):
        """Elimina una asociación de tipo"""
        item = self.session.query(ClienteTipo).get(id_asociacion)
        if item:
            self.session.delete(item)
            self.session.commit()

    # ========== Búsquedas Geográficas (CP/Población) ==========

    def buscar_poblacion_por_cp(self, cp: str, pais: str = "Francia"):
        """
        Busca población por código postal.
        Retorna una tupla: (resultados, db_path, db_config)
        resultados: lista de tuplas (poblacion, provincia)
        db_path: ruta a la BD usada
        db_config: configuración de columnas (para uso en vista si es necesario)
        """
        import sqlite3
        import os
        
        # Map country names to database files and table structures
        country_db_map = {
            'francia': ('france.db', 'villes', 'code_postal', 'nom_standard_majuscule', 'dep_nom'),
            'france': ('france.db', 'villes', 'code_postal', 'nom_standard_majuscule', 'dep_nom'),
            'españa': ('spain.sqlite', 'cp_info', 'cp', 'poblacion', 'provincia'),
            'spain': ('spain.sqlite', 'cp_info', 'cp', 'poblacion', 'provincia'),
            'espagne': ('spain.sqlite', 'cp_info', 'cp', 'poblacion', 'provincia')
        }
        
        db_config = country_db_map.get(pais.lower())
        if not db_config:
            # Default to France if country not found
            db_config = country_db_map['francia']
        
        db_filename, table_name, cp_col, city_col, prov_col = db_config
        
        # Connect to country database
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        db_path = os.path.join(base_dir, 'datos', db_filename)
        
        if not os.path.exists(db_path):
            return [], db_path, db_config
            
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Query for postal code
            cursor.execute(f"""
                SELECT {city_col}, {prov_col} 
                FROM {table_name} 
                WHERE {cp_col} = ? 
                ORDER BY {city_col}
            """, (cp,))
            
            results = cursor.fetchall()
            conn.close()
            
            return results, db_path, db_config
            
        except Exception as e:
            print(f"Error en repositorio buscando población: {e}")
            return [], db_path, db_config

    def buscar_cp_por_poblacion(self, poblacion: str, pais: str = "Francia"):
        """
        Busca códigos postales por nombre de población.
        Retorna una tupla: (resultados, db_path, db_config)
        resultados: lista de tuplas (codigo_postal, poblacion, provincia)
        db_path: ruta a la BD usada
        db_config: configuración de columnas
        """
        import sqlite3
        import os
        
        # Map country names to database files and table structures
        country_db_map = {
            'francia': ('france.db', 'villes', 'code_postal', 'nom_standard_majuscule', 'dep_nom'),
            'france': ('france.db', 'villes', 'code_postal', 'nom_standard_majuscule', 'dep_nom'),
            'españa': ('spain.sqlite', 'cp_info', 'cp', 'poblacion', 'provincia'),
            'spain': ('spain.sqlite', 'cp_info', 'cp', 'poblacion', 'provincia'),
            'espagne': ('spain.sqlite', 'cp_info', 'cp', 'poblacion', 'provincia')
        }
        
        db_config = country_db_map.get(pais.lower())
        if not db_config:
            # Default to France if country not found
            db_config = country_db_map['francia']
        
        db_filename, table_name, cp_col, city_col, prov_col = db_config
        
        # Connect to country database
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        db_path = os.path.join(base_dir, 'datos', db_filename)
        
        if not os.path.exists(db_path):
            return [], db_path, db_config
            
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Query for city name (case-insensitive LIKE search)
            cursor.execute(f"""
                SELECT {cp_col}, {city_col}, {prov_col} 
                FROM {table_name} 
                WHERE {city_col} LIKE ? 
                ORDER BY {city_col}, {cp_col}
                LIMIT 50
            """, (f"%{poblacion.upper()}%",))
            
            results = cursor.fetchall()
            conn.close()
            
            return results, db_path, db_config
            
        except Exception as e:
            print(f"Error en repositorio buscando códigos postales: {e}")
            return [], db_path, db_config
