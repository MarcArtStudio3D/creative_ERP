#!/usr/bin/env python3
"""
Script para traducir creative_erp_fr.ts del español al francés.
Traduce todos los strings marcados como 'unfinished'.
"""

import re
from pathlib import Path

# Diccionario de traducciones español -> francés
TRANSLATIONS = {
    # Términos comunes
    "Dialog": "Dialogue",
    "Cancelar": "Annuler",
    "Aceptar": "Accepter",
    "Guardar": "Enregistrer",
    "Borrar": "Supprimer",
    "Editar": "Modifier",
    "Nuevo": "Nouveau",
    "Buscar": "Rechercher",
    "Salir": "Quitter",
    "Cerrar": "Fermer",
    "Abrir": "Ouvrir",
    "Cambiar": "Changer",
    "Añadir": "Ajouter",
    "Descartar": "Annuler",
    "Deshacer": "Annuler",
    "Anterior": "Précédent",
    "Siguiente": "Suivant",
    "Acceder": "Accéder",
    
    # Avisos
    "Postergar:": "Reporter :",
    "minutos:": "minutes :",
    "horas:": "heures :",
    "dias:": "jours :",
    "Fecha/hora:": "Date/heure :",
    "Aviso:": "Avis :",
    "Dar aviso por cerrado/Recibido.": "Marquer l'avis comme fermé/reçu.",
    
    # Empresas
    "Gestión de empresas": "Gestion des entreprises",
    "Gestión de Empresas": "Gestion des Entreprises",
    "Datos Fiscales y de Gestión": "Données fiscales et de gestion",
    "Web:": "Web :",
    "Inscripción:": "Inscription :",
    "Teléfono 1:": "Téléphone 1 :",
    "Telefono 2:": "Téléphone 2 :",
    "C.P.": "Code postal :",
    "Pais:": "Pays :",
    "Provincia:": "Province :",
    "Dirección:": "Adresse :",
    "Direccion 2:": "Adresse 2 :",
    "Ciudad RCS:": "Ville RCS :",
    "Nº RM:": "N° RM :",
    "SIRET:": "SIRET :",
    "APE/NAF:": "APE/NAF :",
    "TVA non applicable": "TVA non applicable",
    "Codigo:": "Code :",
    "Cif:": "NIF :",
    "Nombre:": "Nom :",
    "Nombre Fiscal:": "Nom fiscal :",
    "Nombre comercial:": "Nom commercial :",
    "Nombre Comercial:": "Nom commercial :",
    "Forma juridica:": "Forme juridique :",
    "Grupo": "Groupe",
    "Mail:": "Email :",
    "Nº RCS:": "N° RCS :",
    "Población:": "Ville :",
    "Movil:": "Mobile :",
    "Móvil:": "Mobile :",
    "Otros datos": "Autres données",
    "Otros": "Autres",
    
    # Formas jurídicas francesas (ya están en francés)
    "EI (Entreprise Individuelle)": "EI (Entreprise Individuelle)",
    "EIRL": "EIRL",
    "Micro-entrepreneur": "Micro-entrepreneur",
    "SARL": "SARL",
    "EURL": "EURL",
    "SAS": "SAS",
    "SASU": "SASU",
    "SA": "SA",
    "SCOP / SCIC": "SCOP / SCIC",
    "SEM": "SEM",
    "RM": "RM",
    
    # Facturas
    "Facturas": "Factures",
    "Digitos Factura:": "Chiffres facture :",
    "Serie Factura:": "Série facture :",
    
    # Divisas
    "Divisas": "Devises",
    "Actualizar divisas al entrar": "Actualiser les devises à l'entrée",
    "Divisa: ": "Devise : ",
    
    # Artículos
    "Articulos": "Articles",
    "Auto codificar los nuevos artículos": "Codifier automatiquement les nouveaux articles",
    "Tamaño del código en caracteres:": "Taille du code en caractères :",
    
    # Decimales
    "Decimales": "Décimales",
    "Decimales en totales": "Décimales dans les totaux",
    "Decimales precios:": "Décimales prix :",
    
    # IRPF
    "IRPF": "Retenue à la source",
    "Autonomo / IRPF": "Indépendant / Retenue",
    "%IRPF:": "% Retenue :",
    
    # Tarifas
    "Tarifas": "Tarifs",
    "Margen Mínimo:": "Marge minimale :",
    "Margen:": "Marge :",
    "Tarifa predeterminada:": "Tarif par défaut :",
    
    # Varios
    "Varios": "Divers",
    "Enlace Web.": "Lien Web.",
    "Gestión Internacional": "Gestion internationale",
    "Cierre ejercicio fiscal:": "Clôture exercice fiscal :",
    "Logotipo": "Logo",
    
    # Comentarios
    "Comentarios": "Commentaires",
    "Comentarios en Albaranes": "Commentaires sur les bons de livraison",
    "Comentarios en Facturas:": "Commentaires sur les factures :",
    
    # Agenda
    "Agenda": "Agenda",
    "Horario Lunes:": "Horaire lundi :",
    "Horario Martes:": "Horaire mardi :",
    "Horario Miercoles:": "Horaire mercredi :",
    "Horario Jueves:": "Horaire jeudi :",
    "Horario Viernes:": "Horaire vendredi :",
    "Horario Sabado:": "Horaire samedi :",
    "Horario Domingo:": "Horaire dimanche :",
    "Acceso a Google Calendar": "Accès à Google Calendar",
    "Google Calendar ID:": "ID Google Calendar :",
    "oauth Acces Token:": "Jeton d'accès OAuth :",
    "oauth Refresh Token:": "Jeton de rafraîchissement OAuth :",
    " Token Expirity:": " Expiration du jeton :",
    
    # Contabilidad
    "Contabilidad": "Comptabilité",
    "Activar contabilidad": "Activer la comptabilité",
    "Digitos cuentas contables:": "Chiffres comptes comptables :",
    "Cientes:": "Clients :",
    "Acreedores:": "Créanciers :",
    "Cuenta de venta de mercaderías:": "Compte de vente de marchandises :",
    "Cuenta de venta (prestación de servicios):": "Compte de vente (prestation de services) :",
    "Proveedores:": "Fournisseurs :",
    "Cuenta IVA soportado": "Compte TVA déductible",
    "Cuenta IVA repercutido": "Compte TVA collectée",
    "IVA soportado RE": "TVA déductible RE",
    "IVA repercutido RE": "TVA collectée RE",
    "Cuenta cobros:": "Compte encaissements :",
    "Cuenta Pagos:": "Compte paiements :",
    
    # Base de datos
    "Datos conexión Base de datos": "Données de connexion à la base de données",
    "Motor Activo de Base de Datos": "Moteur de base de données actif",
    "Datos Acceso MariaDB / MySQL ( Recomendado para empresas entre 2 y 10 ordenadores)": "Données d'accès MariaDB / MySQL (Recommandé pour les entreprises entre 2 et 10 ordinateurs)",
    "Datos Acceso Postgre SQL(Recomendado para empresas con más de 10 ordenadores)": "Données d'accès PostgreSQL (Recommandé pour les entreprises avec plus de 10 ordinateurs)",
    "Nombre Base de Datos:": "Nom de la base de données :",
    "Password:": "Mot de passe :",
    "Puerto:": "Port :",
    "Host:": "Hôte :",
    "Usuario:": "Utilisateur :",
    "Test Database conexion": "Tester la connexion à la base de données",
    "SQLite": "SQLite",
    "MariaDB": "MariaDB",
    "PostgreSQL": "PostgreSQL",
    "MySQL": "MySQL",
    "Ruta BD: Contabilidad:": "Chemin BD : Comptabilité :",
    "...": "...",
    "Migrar a BD Multipuesto": "Migrer vers BD multi-postes",
    "Ruta SQLite Empresa": "Chemin SQLite Entreprise",
    "<html><head/><body><p><span style=\" font-weight:700; color:#ffffff;\">Acceso a SQLite (Para empresas con un solo ordenador)</span></p><p><span style=\" font-weight:700; color:#ffffff;\"><br/></span></p></body></html>": "<html><head/><body><p><span style=\" font-weight:700; color:#ffffff;\">Accès à SQLite (Pour les entreprises avec un seul ordinateur)</span></p><p><span style=\" font-weight:700; color:#ffffff;\"><br/></span></p></body></html>",
    
    # Clientes
    "Gestion de clientes": "Gestion des clients",
    "Cliente:": "Client :",
    "Cliente": "Client",
    "TextLabel": "TextLabel",
    "&Nuevo": "&Nouveau",
    "&Siguiente": "&Suivant",
    "&Anterior": "&Précédent",
    "&Buscar": "&Rechercher",
    "&Editar": "&Modifier",
    "&Guardar": "&Enregistrer",
    "&Deshacer": "&Annuler",
    "Listados": "Listes",
    "B&orrar": "&Supprimer",
    "Nombre": "Nom",
    "Validar VIES": "Valider VIES",
    "CP:": "Code postal :",
    "email:": "email :",
    "Teléfono1:": "Téléphone 1 :",
    "Teléfono 2:": "Téléphone 2 :",
    "Nif IVA:": "N° TVA :",
    "web:": "web :",
    "Código:                        ": "Code :                        ",
    "Observaciones:": "Observations :",
    "Cif/Nif:": "NIF/NIE :",
    "Segundo Apellido:": "Deuxième nom :",
    "Primer Apellido:": "Premier nom :",
    "Otras personas de contacto": "Autres personnes de contact",
    "Personas de contacto": "Personnes de contact",
    "TIPO CLIENTE": "TYPE CLIENT",
    "Editar tipo de cliente": "Modifier le type de client",
    "Tipo": "Type",
    "Direcciones alternativas": "Adresses alternatives",
    "DIRECCIONES": "ADRESSES",
    "Descripción:": "Description :",
    "Población": "Ville",
    "Dirección 2:": "Adresse 2 :",
    "Comentarios:": "Commentaires :",
    "Añadir nueva dirección alternativa": "Ajouter une nouvelle adresse alternative",
    "Borrar una dirección alternativa": "Supprimer une adresse alternative",
    
    # Búsqueda
    "Buscar...": "Rechercher...",
    "Ordenar Por:": "Trier par :",
    "Buscar:": "Rechercher :",
    "Sentido:": "Sens :",
    
    # Configuración
    "Configuración de Creative ERP": "Configuration de Creative ERP",
    "Idioma": "Langue",
    "Español": "Espagnol",
    "Française": "Français",
    "Català": "Catalan",
    "English": "Anglais",
    
    # Login y acceso
    "Creative ERP - Acceso Usuarios": "Creative ERP - Accès utilisateurs",
    "CREATIVE ERP": "CREATIVE ERP",
    "Sistema de Gestión Empresarial": "Système de gestion d'entreprise",
    "Usuario:": "Utilisateur :",
    "Contraseña:": "Mot de passe :",
    "Grupo:": "Groupe :",
    "Empresa:": "Entreprise :",
    "Configuración": "Configuration",
    "Empresas": "Entreprises",
    
    # Módulos
    "Ventas": "Ventes",
    "Compras": "Achats",
    "Almacén": "Entrepôt",
    "Clientes": "Clients",
    "Proveedores": "Fournisseurs",
    "Productos": "Produits",
    "Informes": "Rapports",
    "Administración": "Administration",
    "Configuración y usuarios": "Configuration et utilisateurs",
    "Gestor de Módulos": "Gestionnaire de modules",
    "Gestión de módulos": "Gestion des modules",
    
    # Números de cuenta (mantener)
    "610": "610",
    "600": "600",
    "410": "410",
    "400": "400",
    "430": "430",
    "(F1 - lista)": "(F1 - liste)",
    "E": "E",
    "R": "R",
    "N": "N",
    "SR": "SR",
    "0": "0",
    
    # Adicionales con & (atajos de teclado)
    "&Nuevo": "&Nouveau",
    "&Siguiente": "&Suivant",
    "&Anterior": "&Précédent",
    "&Buscar": "&Rechercher",
    "&Editar": "&Modifier",
    "&Guardar": "&Enregistrer",
    "&Deshacer": "&Annuler",
    "B&orrar": "&Supprimer",
    
    # Datos bancarios
    "Datos Bancarios y Financieros": "Données bancaires et financières",
    "Tarifa Cliente:": "Tarif client :",
    "Divisa:": "Devise :",
    "Forma de Pago:": "Mode de paiement :",
    "Día de pago 1:": "Jour de paiement 1 :",
    "Día de pago 2:": "Jour de paiement 2 :",
    "Porcentaje DTO Fijo:": "Pourcentage remise fixe :",
    "Descuento:": "Remise :",
    "Riesgo Máximo:": "Risque maximum :",
    "Cuenta Contable:": "Compte comptable :",
    "IBAN:": "IBAN :",
    "BIC/SWIFT:": "BIC/SWIFT :",
    "Banco:": "Banque :",
    "Titular:": "Titulaire :",
    
    # Más términos
    "Datos Comerciales": "Données commerciales",
    "Datos Contables": "Données comptables",
    "Datos Adicionales": "Données supplémentaires",
    "Activo": "Actif",
    "Inactivo": "Inactif",
    "Sí": "Oui",
    "No": "Non",
    "Todos": "Tous",
    "Ninguno": "Aucun",
    "Seleccionar": "Sélectionner",
    "Imprimir": "Imprimer",
    "Exportar": "Exporter",
    "Importar": "Importer",
    "Actualizar": "Actualiser",
    "Refrescar": "Rafraîchir",
    "Filtrar": "Filtrer",
    "Limpiar": "Effacer",
    "Aplicar": "Appliquer",
    "Restablecer": "Réinitialiser",
    "Copiar": "Copier",
    "Pegar": "Coller",
    "Cortar": "Couper",
    "Duplicar": "Dupliquer",
    "Mover": "Déplacer",
    "Renombrar": "Renommer",
    "Propiedades": "Propriétés",
    "Detalles": "Détails",
    "Información": "Information",
    "Ayuda": "Aide",
    "Acerca de": "À propos",
    "Versión": "Version",
    "Fecha": "Date",
    "Hora": "Heure",
    "Total": "Total",
    "Subtotal": "Sous-total",
    "Cantidad": "Quantité",
    "Precio": "Prix",
    "Importe": "Montant",
    "IVA": "TVA",
    "Base": "Base",
    "Descuento": "Remise",
    "Recargo": "Majoration",
    
    # Términos de interfaz
    "Aceptar y cerrar": "Accepter et fermer",
    "Cancelar y cerrar": "Annuler et fermer",
    "Sí, continuar": "Oui, continuer",
    "No, cancelar": "Non, annuler",
    "Confirmar": "Confirmer",
    "Rechazar": "Refuser",
    "Omitir": "Ignorer",
    "Reintentar": "Réessayer",
    "Continuar": "Continuer",
    "Finalizar": "Terminer",
    "Siguiente >": "Suivant >",
    "< Anterior": "< Précédent",
    "Terminar": "Terminer",
    "Inicio": "Accueil",
    "Fin": "Fin",
    "Primera página": "Première page",
    "Última página": "Dernière page",
    "Página": "Page",
    "de": "de",
    "Registros": "Enregistrements",
    "Mostrando": "Affichage",
    "a": "à",
    "Filtros": "Filtres",
    "Ordenar": "Trier",
    "Ascendente": "Croissant",
    "Descendente": "Décroissant",
    "Por defecto": "Par défaut",
    "Personalizado": "Personnalisé",
    "Avanzado": "Avancé",
    "Básico": "Basique",
    "Simple": "Simple",
    "Completo": "Complet",
    "Resumido": "Résumé",
    "Detallado": "Détaillé",
}


def translate_ts_file(input_file: Path, output_file: Path):
    """Traduce un archivo .ts del español al francés."""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Contar traducciones realizadas
    translations_count = 0
    
    # Buscar todos los bloques <message> con translation unfinished
    pattern = r'(<message>.*?<source>(.*?)</source>.*?<translation type="unfinished"></translation>.*?</message>)'
    
    def replace_translation(match):
        nonlocal translations_count
        full_block = match.group(1)
        source_text = match.group(2)
        
        # Buscar traducción
        if source_text in TRANSLATIONS:
            translation = TRANSLATIONS[source_text]
            # Reemplazar el bloque completo
            new_block = full_block.replace(
                '<translation type="unfinished"></translation>',
                f'<translation>{translation}</translation>'
            )
            translations_count += 1
            return new_block
        
        return full_block
    
    # Aplicar traducciones
    new_content = re.sub(pattern, replace_translation, content, flags=re.DOTALL)
    
    # Guardar archivo traducido
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return translations_count


def main():
    input_file = Path("translations/creative_erp_fr.ts")
    output_file = input_file  # Sobrescribir el mismo archivo
    
    print("=" * 60)
    print("Traduciendo creative_erp_fr.ts al francés")
    print("=" * 60)
    
    count = translate_ts_file(input_file, output_file)
    
    print(f"\n✓ {count} traducciones aplicadas")
    print(f"✓ Archivo actualizado: {output_file}")
    print("\nPróximo paso:")
    print("  python scripts/compile_translations.py")
    print()


if __name__ == "__main__":
    main()
