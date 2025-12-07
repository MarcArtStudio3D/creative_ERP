# ==========================================
# PLAN DE MIGRACIÓN: SQLAlchemy -> SQLModel
# ==========================================

## 1. DEPENDENCIAS
- [X] requirements.txt - Cambiar SQLAlchemy>=1.4 por sqlmodel>=0.0.14

## 2. ARCHIVOS CORE A MIGRAR

### 2.1 core/models.py
- Cambiar: from sqlalchemy import Column, Integer, String...
- Por: from sqlmodel import SQLModel, Field, Relationship
- Cambiar: Base = declarative_base()
- Por: class Base(SQLModel): pass (no necesario, SQLModel lo maneja)
- Actualizar cada modelo:
  * De: class User(Base):
  * A: class User(SQLModel, table=True):
  * Convertir Column() a Field()
  * Convertir tipos SQLAlchemy a tipos Python con anotaciones

### 2.2 core/db.py  
- Mantener create_engine de SQLAlchemy (SQLModel usa SQLAlchemy internamente)
- Cambiar: from core.models import Base
- Por: from sqlmodel import SQLModel
- Actualizar: Base.metadata.create_all(bind=engine)
- Por: SQLModel.metadata.create_all(bind=engine)
- Actualizar sessionmaker para usar Session de sqlmodel
- De: from sqlalchemy.orm import sessionmaker, scoped_session
- A: from sqlmodel import Session, create_engine

## 3. MÓDULOS A MIGRAR

### 3.1 modules/clientes/models.py
- Migrar modelos de Cliente, Direccion, etc.

### 3.2 modules/clientes/repository.py
- Actualizar queries para usar select() de SQLModel
- De: session.query(Cliente).filter(...)
- A: session.exec(select(Cliente).where(...))

### 3.3 modules/articulos/models.py
- Migrar modelos de Articulo, Seccion, Familia, etc.

### 3.4 modules/articulos/repository.py
- Actualizar queries

### 3.5 modules/empresas/models.py (si existe separado)
- Ya está en core/models.py

### 3.6 modules/facturas/models.py
- Migrar modelos de Factura

### 3.7 modules/tipo_cliente/models.py
- Migrar modelos TipoCliente, SubtipoCliente

### 3.8 modules/divisiones_almacen/models.py
- Migrar modelos Seccion, Familia, Subfamilia

### 3.9 modules/tarifas_maestras/models.py
- Migrar si existe

## 4. TESTS A ACTUALIZAR
- Todos los tests que usan:
  * from sqlalchemy import text
  * session.execute(text(...))
- Estos seguirán funcionando igual (SQLModel usa SQLAlchemy internamente)

## 5. PATRONES DE MIGRACIÓN

### Modelo SQLAlchemy:
```python
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
```

### Modelo SQLModel:
```python
class User(SQLModel, table=True):
    __tablename__ = 'users'
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=50, unique=True, index=True)
    email: Optional[str] = Field(default=None, max_length=100, unique=True)
    is_active: int = Field(default=1)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### Query SQLAlchemy:
```python
user = session.query(User).filter(User.username == 'admin').first()
users = session.query(User).all()
```

### Query SQLModel:
```python
from sqlmodel import select
user = session.exec(select(User).where(User.username == 'admin')).first()
users = session.exec(select(User)).all()
```

### Relationships SQLAlchemy:
```python
group = relationship('BusinessGroup', backref='empresas')
```

### Relationships SQLModel:
```python
group: Optional[BusinessGroup] = Relationship(back_populates="empresas")
```

## 6. VENTAJAS DE SQLMODEL
1. **Validación automática**: Pydantic valida los datos automáticamente
2. **Type hints nativos**: Mejor soporte de IDE y mypy
3. **Menos código**: No necesitas definir tipos dos veces
4. **Serialización JSON**: Automática con .dict() y .json()
5. **Más mantenible**: Código más limpio y pythónico
6. **Compatibilidad**: USA SQLAlchemy internamente, 100% compatible

## 7. ORDEN DE EJECUCIÓN
1. ✓ Actualizar requirements.txt
2. ✓ Crear core/models_new.py con modelos migrados
3. Migrar core/models.py completamente
4. Actualizar core/db.py
5. Migrar modules/clientes/models.py
6. Actualizar modules/clientes/repository.py
7. Migrar modules/articulos/models.py
8. Actualizar modules/articulos/repository.py
9. Migrar resto de módulos
10. Ejecutar tests y corregir errores
11. Limpiar archivos temporales

## 8. COMANDOS ÚTILES
```bash
# Instalar SQLModel
pip install sqlmodel

# Verificar imports
grep -r "from sqlalchemy" --include="*.py" | grep -v test | grep -v alembic

# Buscar queries a actualizar
grep -r "session.query" --include="*.py" | grep -v test
```

## 9. NOTAS IMPORTANTES
- SQLModel usa SQLAlchemy 2.0 internamente
- Las migraciones de Alembic seguirán funcionando
- Los tests con `text()` seguirán funcionando
- Mantener compatibilidad con código existente durante la transición

