from typing import List, Optional
from core.db import get_session
from core.models import Empresa


class EmpresaRepository:
    def __init__(self, session=None):
        self._external_session = session

    def _session(self):
        return self._external_session or get_session()

    def obtener_todos(self) -> List[Empresa]:
        sess = self._session()
        return sess.query(Empresa).order_by(Empresa.nombre_fiscal).all()

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
