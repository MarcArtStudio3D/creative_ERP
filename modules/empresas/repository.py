from typing import List, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.db import get_session, get_database_url
from core.models import Empresa, DireccionAlternativaEmpresa, BusinessGroup


class EmpresaRepository:
    def __init__(self, session=None):
        self._external_session = session
        self._main_session = None
        self._engine = None

    def _session(self):
        # Si se proporcionó una sesión externa, usarla (útil para tests)
        if self._external_session:
            return self._external_session
            
        # Si ya tenemos una sesión dedicada a main, verificar que esté activa
        if self._main_session:
            try:
                # Simple check to see if session is valid
                self._main_session.execute("SELECT 1")
                return self._main_session
            except Exception:
                # Si falla, recrear
                if self._main_session:
                    self._main_session.close()
                self._main_session = None

        # Crear conexión explícita a la base de datos 'main'
        # Esto es necesario porque el contexto global de la app puede estar apuntando
        # a una base de datos de empresa (tenant), pero las empresas siempre están en 'main'.
        try:
            if not self._engine:
                db_url = get_database_url('main')
                self._engine = create_engine(db_url)
            
            Session = sessionmaker(bind=self._engine)
            self._main_session = Session()
            return self._main_session
        except Exception as e:
            print(f"Error connecting to main database: {e}")
            # Fallback to global session if specific connection fails
            return get_session()

    def obtener_todos(self) -> List[Empresa]:
        sess = self._session()
        return sess.query(Empresa).order_by(Empresa.nombre_fiscal).all()
        
    def obtener_grupos(self) -> List[BusinessGroup]:
        """Obtiene todos los grupos empresariales de la BD principal."""
        sess = self._session()
        return sess.query(BusinessGroup).all()

    def obtener_por_id(self, id_: int) -> Optional[Empresa]:
        sess = self._session()
        return sess.query(Empresa).get(id_)

    def guardar(self, empresa: Empresa) -> Empresa:
        sess = self._session()
        sess.add(empresa)
        sess.commit()
        sess.refresh(empresa)
        return empresa

    def borrar(self, empresa: Empresa) -> None:
        sess = self._session()
        sess.delete(empresa)
        sess.commit()

    # Métodos para direcciones alternativas
    def obtener_direcciones_alternativas(self, id_empresa: int) -> List[DireccionAlternativaEmpresa]:
        sess = self._session()
        return sess.query(DireccionAlternativaEmpresa).filter_by(id_empresa=id_empresa).order_by(DireccionAlternativaEmpresa.descripcion).all()

    def obtener_direccion_alternativa_por_id(self, id_direccion: int) -> Optional[DireccionAlternativaEmpresa]:
        sess = self._session()
        return sess.query(DireccionAlternativaEmpresa).get(id_direccion)

    def guardar_direccion_alternativa(self, direccion: DireccionAlternativaEmpresa) -> DireccionAlternativaEmpresa:
        sess = self._session()
        sess.add(direccion)
        sess.commit()
        sess.refresh(direccion)
        return direccion

    def borrar_direccion_alternativa(self, direccion: DireccionAlternativaEmpresa) -> None:
        sess = self._session()
        sess.delete(direccion)
        sess.commit()

    def __del__(self):
        # Cerrar sesión y engine al destruir el repositorio
        if self._main_session:
            try:
                self._main_session.close()
            except:
                pass
        if self._engine:
            try:
                self._engine.dispose()
            except:
                pass
