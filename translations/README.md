# Sistema de Traducciones de Creative ERP

Este documento explica cómo gestionar las traducciones de la aplicación Creative ERP.

## 📁 Estructura de Archivos

```
Creative_ERP/
├── translations/           # Archivos de traducción
│   ├── creative_erp_es.ts # Español (fuente)
│   ├── creative_erp_en.ts # Inglés
│   ├── creative_erp_ca.ts # Catalán
│   ├── creative_erp_es.qm # Español compilado
│   ├── creative_erp_en.qm # Inglés compilado
│   └── creative_erp_ca.qm # Catalán compilado
├── scripts/
│   ├── extract_all_strings.py      # Extrae strings del código
│   ├── compile_translations.py     # Compila .ts a .qm
│   ├── generate_translations.sh    # Script bash (alternativo)
│   └── compile_translations.sh     # Script bash (alternativo)
├── core/
│   └── translations.py    # Módulo de carga de traducciones
└── creative_erp.pro       # Configuración de Qt
```

## 🚀 Inicio Rápido

### 1. Generar archivos de traducción

Extrae todos los strings de la interfaz de usuario:

```bash
python scripts/extract_all_strings.py
```

Esto creará/actualizará los archivos `.ts` en el directorio `translations/`.

---

## 🇫🇷 Guide de Traduction en Français

### 1. Générer les fichiers de traduction

Extrayez toutes les chaînes de l'interface utilisateur :

```bash
python scripts/extract_all_strings.py
```

Cela créera/mettra à jour les fichiers `.ts` dans le répertoire `translations/`.

### 2. Traduire les textes

Vous avez deux options :

#### Option A : Qt Linguist (Recommandé)

Qt Linguist est un outil graphique qui facilite la traduction :

```bash
# Installer Qt Linguist
sudo apt-get install qttools5-dev-tools  # Ubuntu/Debian
brew install qt                           # macOS

# Ouvrir le fichier de traduction française
linguist translations/creative_erp_fr.ts
```

**Utilisation de Qt Linguist :**
1. Ouvrez le fichier `.ts` avec Qt Linguist
2. Sélectionnez chaque chaîne dans la liste
3. Entrez la traduction française dans le champ "Traduction"
4. Marquez la traduction comme "Terminée" (icône ✓)
5. Sauvegardez le fichier (Ctrl+S)

#### Option B : Édition manuelle

Les fichiers `.ts` sont au format XML et peuvent être édités avec n'importe quel éditeur de texte :

```xml
<message>
    <source>Ventas</source>
    <translation type="unfinished"></translation>
</message>
```

Changez en :

```xml
<message>
    <source>Ventas</source>
    <translation>Ventes</translation>
</message>
```

### 3. Compiler les traductions

Une fois les fichiers `.ts` traduits, compilez-les en `.qm` :

```bash
python scripts/compile_translations.py
```

Cela générera les fichiers `.qm` utilisés par l'application.

### 4. Utiliser les traductions dans l'application

Modifiez `app/app.py` en suivant l'exemple dans `translations/INTEGRATION_EXAMPLE.py` :

```python
from PySide6.QtWidgets import QApplication
from core.translations import load_translation
import sys

app = QApplication(sys.argv)

# Charger la traduction (détecte automatiquement la langue du système)
translator = load_translation(app)

# Ou spécifier une langue manuellement
# translator = load_translation(app, 'fr')  # Français
```

### 5. Tester l'application en français

```bash
# Forcer l'application à utiliser le français
LANG=fr_FR.UTF-8 python main.py

# Ou modifier le code pour utiliser le français par défaut
```

---

## 🌍 Idiomas Disponibles / Langues Disponibles

### 2. Traducir los textos

Tienes dos opciones:

#### Opción A: Qt Linguist (Recomendado)

Qt Linguist es una herramienta gráfica que facilita la traducción:

```bash
# Instalar Qt Linguist
sudo apt-get install qttools5-dev-tools  # Ubuntu/Debian
brew install qt                           # macOS

# Abrir archivo de traducción
linguist translations/creative_erp_en.ts
```

#### Opción B: Edición manual

Los archivos `.ts` son XML y pueden editarse con cualquier editor de texto:

```xml
<message>
    <source>Ventas</source>
    <translation type="unfinished"></translation>
</message>
```

Cambia a:

```xml
<message>
    <source>Ventas</source>
    <translation>Sales</translation>
</message>
```

### 3. Compilar las traducciones

Una vez traducidos los archivos `.ts`, compílalos a `.qm`:

```bash
python scripts/compile_translations.py
```

Esto generará los archivos `.qm` que usa la aplicación.

### 4. Usar las traducciones en la aplicación

Modifica `app/app.py` o `main.py` para cargar las traducciones:

```python
from PySide6.QtWidgets import QApplication
from core.translations import load_translation
import sys

app = QApplication(sys.argv)

# Cargar traducción (automáticamente detecta el idioma del sistema)
translator = load_translation(app)

# O especificar un idioma manualmente
# translator = load_translation(app, 'en')  # Inglés
# translator = load_translation(app, 'ca')  # Catalán

# ... resto de tu código
```

## 🌍 Idiomas Disponibles / Langues Disponibles

| Código | Idioma   | Langue    | Estado / Statut |
|--------|----------|-----------|-----------------|
| `es`   | Español  | Espagnol  | ✅ Completo (idioma base) |
| `en`   | English  | Anglais   | ⚠️ Requiere traducción / Nécessite traduction |
| `ca`   | Català   | Catalan   | ⚠️ Requiere traducción / Nécessite traduction |
| `fr`   | Français | Français  | ⚠️ Requiere traducción / Nécessite traduction |

## 📝 Workflow de Traducción

### Flujo completo

1. **Desarrollar**: Escribe tu código en español (idioma base)
2. **Extraer**: `python scripts/extract_all_strings.py`
3. **Traducir**: Edita los archivos `.ts` con Qt Linguist o manualmente
4. **Compilar**: `python scripts/compile_translations.py`
5. **Probar**: Ejecuta la aplicación en diferentes idiomas

### Actualizar traducciones existentes

Cuando añades nuevos textos al código:

```bash
# 1. Extraer nuevos strings (mantiene traducciones existentes)
python scripts/extract_all_strings.py

# 2. Traducir solo los nuevos strings marcados como "unfinished"
linguist translations/creative_erp_en.ts

# 3. Compilar
python scripts/compile_translations.py
```

## 🔧 Configuración Avanzada

### Añadir un nuevo idioma

1. Edita `creative_erp.pro` y añade el nuevo idioma:

```
TRANSLATIONS = translations/creative_erp_es.ts \
               translations/creative_erp_en.ts \
               translations/creative_erp_ca.ts \
               translations/creative_erp_fr.ts
```

2. Edita `scripts/extract_all_strings.py` y añade el idioma:

```python
languages = {
    'es': 'Español',
    'en': 'English',
    'ca': 'Català',
    'fr': 'Français'  # Nuevo
}
```

3. Edita `core/translations.py` y añade el idioma:

```python
AVAILABLE_LANGUAGES = {
    'es': 'Español',
    'en': 'English',
    'ca': 'Català',
    'fr': 'Français',  # Nuevo
}
```

4. Genera y traduce:

```bash
python scripts/extract_all_strings.py
linguist translations/creative_erp_fr.ts
python scripts/compile_translations.py
```

### Cambiar idioma en tiempo de ejecución

```python
from core.translations import change_language

# En tu código de configuración o menú
new_translator = change_language(app, old_translator, 'en')
```

## 🎯 Mejores Prácticas

### 1. Usar self.tr() para nuevos textos

Para que las traducciones funcionen mejor en el futuro, marca los textos con `self.tr()`:

```python
# ❌ Antes
label = QLabel("Ventas")

# ✅ Después
label = QLabel(self.tr("Ventas"))
```

### 2. Contexto en traducciones

El contexto (nombre de clase) ayuda a traducir correctamente:

```python
class VentasWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # El contexto será "VentasWindow"
        self.setWindowTitle(self.tr("Ventas"))
```

### 3. Strings con variables

Para textos con variables, usa placeholders:

```python
# ❌ Evitar
message = f"Bienvenido, {username}"

# ✅ Mejor
message = self.tr("Bienvenido, %1").arg(username)
```

### 4. Plurales

Qt soporta formas plurales:

```python
count = 5
message = self.tr("%n módulo(s)", "", count)
```

## 🐛 Solución de Problemas

### Los archivos .qm no se generan

Asegúrate de tener `lrelease` instalado:

```bash
# Ubuntu/Debian
sudo apt-get install qttools5-dev-tools

# macOS
brew install qt

# Verificar instalación
lrelease -version
```

### Las traducciones no se cargan

1. Verifica que los archivos `.qm` existen en `translations/`
2. Comprueba que el código de idioma es correcto
3. Asegúrate de llamar a `load_translation()` antes de crear las ventanas

### Strings no se extraen

El script actual extrae strings de:
- Constructores de widgets Qt
- Métodos `setText()`, `setWindowTitle()`, etc.
- Diccionarios con claves comunes

Si un string no se extrae, puedes:
1. Añadirlo manualmente al archivo `.ts`
2. Modificar `scripts/extract_all_strings.py` para incluir más patrones

## 📚 Recursos

- [Qt Linguist Manual](https://doc.qt.io/qt-6/qtlinguist-index.html)
- [Qt Translation Tutorial](https://doc.qt.io/qt-6/internationalization.html)
- [PySide6 i18n Guide](https://doc.qt.io/qtforpython-6/tutorials/basictutorial/translations.html)

## 📄 Licencia

Las traducciones siguen la misma licencia que Creative ERP.
