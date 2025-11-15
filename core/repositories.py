# -----------------------------
# core/repositories.py
# -----------------------------
from .db import SessionLocal
from .models import Client, Invoice


class ClientRepo:
@staticmethod
def get_all():
db = SessionLocal()
return db.query(Client).all()


@staticmethod
def create(**kwargs):
db = SessionLocal()
c = Client(**kwargs)
db.add(c)
db.commit()
db.refresh(c)
return c


class InvoiceRepo:
@staticmethod
def create(**kwargs):
db = SessionLocal()
inv = Invoice(**kwargs)
db.add(inv)
db.commit()
db.refresh(inv)
return inv