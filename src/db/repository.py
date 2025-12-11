import sqlite3
import dataclasses
import typing
from typing import Type, Any, get_origin, get_args

class Repository:
    def __init__(self, db_path: str, model: Type[Any], table: str = None):
        self.db_path = db_path
        self.model = model
        self.table = table or model.__name__.lower()
        self._ensure_table()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _py_type_to_sql(self, t):
        # Maneja Optional[T] y tipos básicos
        orig = get_origin(t)
        if orig is typing.Union:
            args = get_args(t)
            non_none = [a for a in args if a is not type(None)]
            if non_none:
                return self._py_type_to_sql(non_none[0])
        if t in (int,):
            return "INTEGER"
        if t in (float,):
            return "REAL"
        return "TEXT"

    def _ensure_table(self):
        cols = []
        for f in dataclasses.fields(self.model):
            sqltype = self._py_type_to_sql(f.type)
            if f.name == "id" and sqltype == "INTEGER":
                cols.append("id INTEGER PRIMARY KEY AUTOINCREMENT")
            else:
                cols.append(f"{f.name} {sqltype}")
        sql = f"CREATE TABLE IF NOT EXISTS {self.table} ({', '.join(cols)})"
        with self._connect() as conn:
            conn.execute(sql)

    def save(self, instance: Any):
        d = dataclasses.asdict(instance)
        # Si id es None, lo excluimos para que AUTOINCREMENT lo asigne
        keys = [k for k, v in d.items() if not (k == "id" and v is None)]
        vals = [d[k] for k in keys]
        placeholders = ", ".join(["?"] * len(keys)) if keys else ""
        if keys:
            sql = f"INSERT INTO {self.table} ({', '.join(keys)}) VALUES ({placeholders})"
            with self._connect() as conn:
                cur = conn.cursor()
                cur.execute(sql, vals)
                if 'id' in d and d.get('id') is None:
                    instance.id = cur.lastrowid
                conn.commit()
        return instance

    def get_by_id(self, id_):
        sql = f"SELECT * FROM {self.table} WHERE id=?"
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(sql, (id_,))
            row = cur.fetchone()
            if not row:
                return None
            cols = [c[0] for c in cur.description]
            data = dict(zip(cols, row))
            return self.model(**data)

    def list_all(self):
        sql = f"SELECT * FROM {self.table}"
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            cols = [c[0] for c in cur.description]
            return [self.model(**dict(zip(cols, row))) for row in rows]

