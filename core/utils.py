"""
Utilidades comunes para formateo numérico y configuración por empresa.
"""

from __future__ import annotations

from datetime import date as _date_type
from typing import Dict, Optional

from PySide6.QtCore import QDate


def qdate_to_date(qd) -> Optional[_date_type]:
    """Convertir un QDate a datetime.date de forma segura.

    - Si qd es None o inválido, devuelve None.
    - Si QDate implementa toPython(), lo usa y devuelve el resultado.
    - Si no, intenta construir manualmente datetime.date(qd.year(), qd.month(), qd.day()).

    Está pensado para uso desde las vistas para evitar duplicar lógica.
    """
    if qd is None:
        return None

    try:
        # isValid existe en QDate; comprobar antes de convertir
        if hasattr(qd, "isValid") and not qd.isValid():
            return None

        # Preferir toPython() cuando está disponible
        try:
            return qd.toPython()
        except Exception:
            from datetime import date as _date

            try:
                return _date(qd.year(), qd.month(), qd.day())
            except Exception:
                return None
    except Exception:
        return None


def format_decimal_value(value, decimals: int = 2, use_comma: bool = True) -> str:
    """Formato seguro para mostrar números en UI.

    - value: número o cadena convertible a float.
    - decimals: número de decimales a mostrar.
    - use_comma: si True, utiliza coma como separador decimal (UI). Si False, usa punto.

    Devuelve la representación en cadena con el separador elegido.
    """
    try:
        d = int(decimals)
    except Exception:
        d = 2

    # Convertir a float si es posible
    try:
        num = float(value)
    except Exception:
        # No es numérico -> devolver tal cual
        return str(value)

    formatted = f"{num:.{d}f}"
    if use_comma:
        return formatted.replace(".", ",")
    return formatted


def parse_decimal_input(text: str) -> float:
    """Parse a user-entered number string and return a float.

    Heuristics supported:
    - '1.234,56' -> 1234.56 (dot as thousands, comma as decimal)
    - '1,234.56' -> 1234.56 (comma as thousands, dot as decimal)
    - '350,50' -> 350.50
    - '350.50' -> 350.50
    - '1234' -> 1234.0

    Falls back to float() where possible, otherwise raises ValueError.
    """
    if text is None:
        raise ValueError("No input")

    s = str(text).strip()
    if s == "":
        raise ValueError("Empty input")

    # Detect both separators present
    has_dot = "." in s
    has_comma = "," in s

    # If both present, assume the last one is the decimal separator
    if has_dot and has_comma:
        # decide based on position: rightmost separator is decimal
        last_dot = s.rfind(".")
        last_comma = s.rfind(",")
        if last_comma > last_dot:
            # comma is decimal, remove dots
            normalized = s.replace(".", "")
            normalized = normalized.replace(",", ".")
        else:
            # dot is decimal, remove commas
            normalized = s.replace(",", "")
    else:
        # Only comma present -> comma is decimal
        if has_comma:
            normalized = s.replace(".", "").replace(",", ".")
        else:
            # Only dot or no separator -> try converting directly
            normalized = s

    # Final cleanup: remove spaces
    normalized = normalized.replace(" ", "")

    # Attempt float conversion
    try:
        return float(normalized)
    except Exception as e:
        raise ValueError(f"Cannot parse number: {text}") from e


def get_company_decimal_settings(
    default_totales: int = 2, default_precios: int = 2
) -> Dict[str, int]:
    """Lee las preferencias de decimales para la empresa actualmente seleccionada.

    Retorna dict con claves 'decimales_totales' y 'decimales_precios'.
    No cambia la base de datos actual a largo plazo; realiza cambios puntuales para leer desde `main`.
    """
    try:
        from core.company_manager import get_current_company_context
        from core.db import get_current_database, get_session, set_current_database
        from core.models import Empresa

        ctx = get_current_company_context()
        if not ctx.get("has_company"):
            return {
                "decimales_totales": default_totales,
                "decimales_precios": default_precios,
            }

        company_id = ctx.get("company_id")
        if not company_id:
            return {
                "decimales_totales": default_totales,
                "decimales_precios": default_precios,
            }

        original_db = get_current_database()
        set_current_database("main")
        session = get_session()
        try:
            empresa = session.query(Empresa).filter_by(id=company_id).first()
            if not empresa:
                return {
                    "decimales_totales": default_totales,
                    "decimales_precios": default_precios,
                }

            return {
                "decimales_totales": int(
                    getattr(empresa, "decimales_totales", default_totales)
                    or default_totales
                ),
                "decimales_precios": int(
                    getattr(empresa, "decimales_precios", default_precios)
                    or default_precios
                ),
            }
        finally:
            try:
                session.close()
            except Exception:
                pass
            set_current_database(original_db)
    except Exception:
        return {
            "decimales_totales": default_totales,
            "decimales_precios": default_precios,
        }


def pydate_to_qdate(d) -> QDate:
    """Convertir un objeto date/datetime/objeto con atributos year/month/day a QDate.

    - Acepta: None, QDate, datetime.date, datetime.datetime, y objetos que expongan
      year/month/day como atributos o métodos.
    - Devuelve QDate() (vacío) en caso de fallo o valores no válidos.
    """
    if not d:
        return QDate()
    try:
        if isinstance(d, QDate):
            return d

        def _get_int(o, name):
            v = getattr(o, name, None)
            if callable(v):
                try:
                    v = v()
                except Exception:
                    v = None
            try:
                return int(v)
            except Exception:
                return 0

        y = _get_int(d, "year")
        m = _get_int(d, "month")
        day = _get_int(d, "day")

        if y <= 0 or m <= 0 or day <= 0:
            return QDate()
        return QDate(y, m, day)
    except Exception:
        return QDate()
