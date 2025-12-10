# 🧪 GUÍA DE TESTING MANUAL

## Módulo de Clientes - Verificación Funcional

### Pre-requisitos
- ✅ Aplicación ejecutándose
- ✅ Usuario con permisos de acceso
- ✅ Base de datos con clientes de prueba

---

## TEST 1: Visualización de Tabla ✅

**Objetivo**: Verificar que la tabla de clientes muestra datos correctamente

**Pasos**:
1. Abrir la aplicación
2. Hacer login (usuario: admin, empresa: Artstudio3d)
3. Ir al módulo de Clientes

**Resultado esperado**:
- ✅ Se muestra la tabla con clientes
- ✅ Columnas visibles: Código, CIF/NIF, Nombre Fiscal, Teléfono, Email
- ✅ Los datos se ven correctamente
- ✅ No hay errores en consola

---

## TEST 2: Intento de Edición Directa ❌

**Objetivo**: Verificar que NO se puede editar en la tabla

**Pasos**:
1. Hacer click en una celda de la tabla
2. Intentar escribir texto
3. Hacer doble click en una celda

**Resultado esperado**:
- ❌ NO se puede escribir en la celda
- ❌ NO aparece cursor de edición
- ✅ Se mantiene en modo lectura

---

## TEST 3: Doble Click - Cambio de Página ✅

**Objetivo**: Verificar que el doble click cambia a la página de edición

**Pasos**:
1. Hacer doble click en una fila de la tabla
2. Observar qué sucede

**Resultado esperado**:
- ✅ La vista cambia a la página de edición (formulario)
- ✅ Ya no se ve la tabla
- ✅ Se ven los campos del formulario
- ✅ Transición suave

---

## TEST 4: Carga de Datos Básicos ✅

**Objetivo**: Verificar que se cargan los datos principales del cliente

**Pasos**:
1. Hacer doble click en un cliente de la tabla
2. Revisar los campos del formulario

**Resultado esperado**:
- ✅ `txtcodigo_cliente`: Muestra el código
- ✅ `txtcif_nif`: Muestra el CIF/NIF
- ✅ `txtnombre`: Muestra el nombre
- ✅ `txtPrimerApellido`: Muestra primer apellido
- ✅ `txtSegundoApellido`: Muestra segundo apellido
- ✅ `txtnombre_fiscal`: Muestra nombre fiscal
- ✅ `txtnombre_comercial`: Muestra nombre comercial

---

## TEST 5: Carga de Dirección ✅

**Objetivo**: Verificar que se carga la dirección completa

**Pasos**:
1. Continuar con el cliente cargado en TEST 4
2. Revisar campos de dirección

**Resultado esperado**:
- ✅ `txtdireccion1`: Muestra dirección línea 1
- ✅ `txtdireccion2`: Muestra dirección línea 2
- ✅ `txtcp`: Muestra código postal
- ✅ `txtpoblacion`: Muestra población
- ✅ `txtprovincia`: Muestra provincia

---

## TEST 6: Carga de Contacto ✅

**Objetivo**: Verificar que se cargan los datos de contacto

**Pasos**:
1. Continuar con el cliente cargado
2. Revisar campos de contacto

**Resultado esperado**:
- ✅ `txttelefono1`: Muestra teléfono 1
- ✅ `txttelefono2`: Muestra teléfono 2
- ✅ `txtmovil`: Muestra móvil
- ✅ `txtemail`: Muestra email
- ✅ `txtweb`: Muestra web (si existe)

---

## TEST 7: Carga de Combos ✅

**Objetivo**: Verificar que los combos se seleccionan correctamente

**Pasos**:
1. Continuar con el cliente cargado
2. Revisar combos desplegables

**Resultado esperado**:
- ✅ `cboDivisa`: Selecciona la divisa correcta
- ✅ `cboforma_pago`: Selecciona forma de pago correcta
- ✅ `cbotarifa_cliente`: Selecciona tarifa correcta (si existe)
- ✅ `cboagente`: Selecciona agente correcto (si existe)

---

## TEST 8: Navegación entre Clientes ✅

**Objetivo**: Verificar que se puede navegar entre clientes

**Pasos**:
1. Con un cliente cargado, hacer click en "Siguiente"
2. Observar los datos
3. Hacer click en "Anterior"
4. Observar los datos

**Resultado esperado**:
- ✅ Botón "Siguiente" carga el siguiente cliente
- ✅ Los datos cambian correctamente
- ✅ Botón "Anterior" carga el cliente anterior
- ✅ Los datos del primer cliente se muestran nuevamente

---

## TEST 9: Volver a Lista ✅

**Objetivo**: Verificar que se puede volver a la tabla

**Pasos**:
1. Con un cliente cargado en edición
2. Hacer click en "Buscar" o "Listados"

**Resultado esperado**:
- ✅ La vista cambia a la tabla
- ✅ Se ve la lista de clientes
- ✅ El cliente que estábamos viendo está seleccionado

---

## TEST 10: Múltiples Clientes ✅

**Objetivo**: Verificar que funciona con diferentes clientes

**Pasos**:
1. En la tabla, hacer doble click en cliente 1
2. Verificar datos cargados
3. Volver a lista
4. Hacer doble click en cliente 2
5. Verificar datos cargados
6. Volver a lista
7. Hacer doble click en cliente 3
8. Verificar datos cargados

**Resultado esperado**:
- ✅ Cada cliente muestra sus propios datos
- ✅ No hay "contaminación" de datos entre clientes
- ✅ Todos los campos se actualizan correctamente
- ✅ Los combos se seleccionan según cada cliente

---

## 🐛 TROUBLESHOOTING

### Problema: La tabla no muestra datos

**Posibles causas**:
- Base de datos vacía
- Error de conexión
- Permisos insuficientes

**Solución**:
```bash
# Verificar que hay clientes en la BD
mysql -uadmin -padmin123 artstudio3d -e "SELECT COUNT(*) FROM clientes;"
```

---

### Problema: Doble click no hace nada

**Posibles causas**:
- Evento no conectado
- stackedWidget no existe

**Solución**:
```python
# Revisar en consola si hay errores
# Verificar que stackedWidget existe en la UI
```

---

### Problema: Los campos no cargan datos

**Posibles causas**:
- ID no guardado en modelo
- Método _get_str() no funciona con dict
- Cliente no encontrado

**Solución**:
- Verificar que items[0].setData(id) se ejecuta
- Verificar que _get_str() tiene isinstance(obj, dict)
- Verificar que obtener_cliente() devuelve datos

---

### Problema: Combos no se seleccionan

**Posibles causas**:
- IDs no coinciden
- itemData no configurado
- _get_value() no funciona

**Solución**:
- Verificar que _get_value() devuelve el ID correcto
- Verificar que los combos tienen itemData configurado
- Debug: print(id_divisa) para ver qué valor tiene

---

## 📝 REGISTRO DE TESTING

### Fecha: _____________

| Test | Resultado | Comentarios |
|------|-----------|-------------|
| TEST 1: Visualización | ☐ PASS ☐ FAIL | |
| TEST 2: Edición Directa | ☐ PASS ☐ FAIL | |
| TEST 3: Cambio Página | ☐ PASS ☐ FAIL | |
| TEST 4: Datos Básicos | ☐ PASS ☐ FAIL | |
| TEST 5: Dirección | ☐ PASS ☐ FAIL | |
| TEST 6: Contacto | ☐ PASS ☐ FAIL | |
| TEST 7: Combos | ☐ PASS ☐ FAIL | |
| TEST 8: Navegación | ☐ PASS ☐ FAIL | |
| TEST 9: Volver Lista | ☐ PASS ☐ FAIL | |
| TEST 10: Múltiples | ☐ PASS ☐ FAIL | |

### Resultado Global: ☐ APROBADO ☐ RECHAZADO

### Observaciones:
```
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________
```

### Tester: _______________ Fecha: _______________

---

## ✅ CRITERIOS DE ACEPTACIÓN

Para considerar el testing **APROBADO**, todos los tests deben pasar:

- ✅ 10/10 tests en PASS
- ✅ Sin errores en consola
- ✅ Sin warnings críticos
- ✅ Rendimiento aceptable (<2s carga)
- ✅ UX intuitiva y fluida

---

## 📞 SOPORTE

Si encuentras problemas:

1. **Revisar logs**: `logs/creative_erp_dev.log`
2. **Revisar consola**: Output de Python
3. **Revisar documentación**: Archivos .md en el proyecto
4. **Crear issue**: Con descripción detallada y pasos para reproducir

---

**Última actualización**: 2025-12-10  
**Versión**: 1.0  
**Estado**: ✅ Listo para testing

