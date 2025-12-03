from typing import Optional
from modules.articulos.repository import ArticuloRepository


class TarifaTipoController:
    """Controller para manejar la tabla tarifas_tipo (tipos de tarifa)."""
    def __init__(self, repository: Optional[ArticuloRepository] = None):
        self.repository = repository or ArticuloRepository()
        self.current: dict | None = None
        self.index_list: list[dict] = []
        self.current_index = -1

    def list_all(self) -> list:
        try:
            res = self.repository.get_tarifa_tipos()
            self.index_list = res
            self.current_index = 0 if res else -1
            self.current = res[0] if res else None
            return res
        except Exception as e:
            print(f"Error listing tarifa tipos: {e}")
            return []

    def load_by_id(self, tipo_id: int) -> bool:
        try:
            data = self.repository.get_tarifa_tipo(tipo_id)
            if data:
                self.current = data
                # set index if present in index_list
                for i, item in enumerate(self.index_list):
                    if item.get('id') == tipo_id:
                        self.current_index = i
                        break
                return True
            return False
        except Exception as e:
            print(f"Error loading tarifa tipo {tipo_id}: {e}")
            return False

    def create(self, payload: dict) -> int | None:
        try:
            new_id = self.repository.create_tarifa_tipo(payload)
            # refresh list
            self.list_all()
            # set current to created
            if new_id:
                self.load_by_id(int(new_id))
            return new_id
        except Exception as e:
            print(f"Error creating tarifa tipo: {e}")
            return None

    def update(self, tipo_id: int, payload: dict) -> bool:
        try:
            ok = self.repository.update_tarifa_tipo(tipo_id, payload)
            if ok:
                self.list_all()
                self.load_by_id(tipo_id)
            return ok
        except Exception as e:
            print(f"Error updating tarifa tipo: {e}")
            return False

    def delete(self, tipo_id: int) -> bool:
        try:
            ok = self.repository.delete_tarifa_tipo(tipo_id)
            if ok:
                self.list_all()
                # adjust current index
                if self.index_list:
                    self.current_index = min(self.current_index, len(self.index_list) - 1)
                    self.current = self.index_list[self.current_index]
                else:
                    self.current_index = -1
                    self.current = None
            return ok
        except Exception as e:
            print(f"Error deleting tarifa tipo: {e}")
            return False

    def next(self) -> bool:
        if not self.index_list:
            return False
        if self.current_index + 1 < len(self.index_list):
            self.current_index += 1
            self.current = self.index_list[self.current_index]
            return True
        return False

    def prev(self) -> bool:
        if not self.index_list:
            return False
        if self.current_index - 1 >= 0:
            self.current_index -= 1
            self.current = self.index_list[self.current_index]
            return True
        return False
