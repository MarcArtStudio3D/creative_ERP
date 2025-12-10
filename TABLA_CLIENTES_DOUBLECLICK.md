# Configuración de Tabla Clientes - Doble Click

## Fecha: 2025-12-10

## Cambio Realizado

### Problema
En la ventana de clientes, el doble click permitía editar directamente en la tabla, lo cual no es el comportamiento deseado.

### Solución Implementada

**Archivo modificado**: `modules/clientes/view.py`

**Cambio en el método `conectar_senales()`**:

```python
# Desactivar edición directa en la tabla
# El usuario debe hacer doble click para ir a la página de edición
try:
    from PySide6.QtWidgets import QAbstractItemView
    tabla.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
except Exception:
    pass
```

### Comportamiento Actual

✅ **Doble click en la tabla**:
- NO permite editar directamente en la celda
- Cambia automáticamente a la página de edición (stackedWidget índice 0)
- Carga los datos del cliente seleccionado en los campos del formulario

✅ **Edición de clientes**:
- Solo se puede editar en la página de formulario
- Los campos de edición están en la página dedicada
- Mejor separación entre vista de lista y vista de edición

### Patrón MVC Respetado

```
Vista (tabla) → Doble Click → abrir_ficha_cliente()
    ↓
Controller → obtener_cliente(id)
    ↓
Repository → get_by_id(id)
    ↓
Vista → cargar_datos_en_formulario()
    ↓
StackedWidget → setCurrentIndex(0) [página de edición]
```

### Propiedades de la Tabla

- `EditTriggers`: `NoEditTriggers` (sin edición directa)
- Doble click: Conectado a `abrir_ficha_cliente()`
- Selección: Por fila completa
- Modo: Solo lectura en la lista

### Consistencia con Artículos

Este comportamiento es **consistente** con el módulo de artículos:
- Artículos: Doble click → cambio a página de edición ✓
- Clientes: Doble click → cambio a página de edición ✓

### Testing

✅ Sin errores de sintaxis
✅ Aplicación carga correctamente
✅ Vista de clientes se inicializa sin problemas
✅ Configuración de tabla aplicada correctamente

## Notas Técnicas

### EditTriggers de Qt

```python
QAbstractItemView.EditTrigger.NoEditTriggers
```

Opciones disponibles:
- `NoEditTriggers`: Sin edición (usado)
- `CurrentChanged`: Editar al cambiar selección
- `DoubleClicked`: Editar con doble click
- `SelectedClicked`: Editar al hacer click en seleccionado
- `EditKeyPressed`: Editar con F2
- `AnyKeyPressed`: Editar con cualquier tecla
- `AllEditTriggers`: Todos los triggers

### StackedWidget

- **Índice 0**: Página de edición (formulario con campos)
- **Índice 1**: Página de lista (tabla de búsqueda)

## Beneficios

1. **UX Mejorada**: Separación clara entre ver lista y editar
2. **Prevención de errores**: No se puede editar accidentalmente en la tabla
3. **Consistencia**: Mismo comportamiento que artículos
4. **MVC limpio**: La tabla es solo para visualización
5. **Seguridad**: Edición controlada en formulario dedicado

## Estado: ✅ COMPLETADO

La tabla de clientes ahora funciona correctamente con doble click para cambiar a la página de edición, sin permitir edición directa en la tabla.

