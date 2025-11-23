#!/usr/bin/env python3
"""
Script para traducir automáticamente todas las cadenas del archivo .ts al francés
"""
import xml.etree.ElementTree as ET

# Diccionario COMPLETO de traducciones español -> francés
translations = {
    # ========== BOTONES PRINCIPALES ==========
    "&Nuevo": "&Nouveau",
    "&Siguiente": "&Suivant",
    "&Anterior": "&Précédent",
    "&Buscar": "&Rechercher",
    "&Editar": "&Modifier",
    "&Guardar": "&Enregistrer",
    "&Deshacer": "&Annuler",
    "B&orrar": "S&upprimer",
    "Listados": "Listes",
    "Aceptar": "Accepter",
    "&Aceptar": "&Accepter",
    "Cancelar": "Annuler",
    "Guardar": "Enregistrer",
    "Deshacer": "Annuler",
    "Nuevo": "Nouveau",
    "Editar": "Modifier",
    "Borrar": "Supprimer",
    "Salir": "Quitter",
    
    # ========== VENTANA DE LOGIN ==========
    "Creative ERP - Acceso Usuarios": "Creative ERP - Accès Utilisateurs",
    "Sistema de Gestión Empresarial": "Système de Gestion d'Entreprise",
    "Usuario:": "Utilisateur :",
    "Contraseña:": "Mot de passe :",
    "Grupo:": "Groupe :",
    "Empresa:": "Entreprise :",
    "Acceder": "Accéder",
    "Cerrar": "Fermer",
    "⚙️\nConfiguración": "⚙️\nConfiguration",
    "Error": "Erreur",
    "Ingresa usuario y contraseña": "Saisissez l'utilisateur et le mot de passe",
    "Selecciona grupo y empresa": "Sélectionnez le groupe et l'entreprise",
    "Usuario o contraseña incorrectos": "Utilisateur ou mot de passe incorrect",
    "Idioma cambiado a": "Langue changée en",
    "Cambio de idioma": "Changement de langue",
    "La aplicación debe reiniciarse para aplicar todos los cambios": "L'application doit être redémarrée pour appliquer tous les changements",
    
    # ========== VENTANA PRINCIPAL ==========
    "Creative ERP - Sistema de Gestión Empresarial": "Creative ERP - Système de Gestion d'Entreprise",
    "MÓDULOS": "MODULES",
    "Ventas": "Ventes",
    "Gestión de clientes y facturación": "Gestion des clients et facturation",
    "Compras": "Achats",
    "Proveedores y facturas de compra": "Fournisseurs et factures d'achat",
    "Almacén": "Entrepôt",
    "Inventario y control de stock": "Inventaire et contrôle des stocks",
    "Financiero": "Financier",
    "Contabilidad y tesorería": "Comptabilité et trésorerie",
    "Proyectos": "Projets",
    "Gestión de proyectos creativos": "Gestion de projets créatifs",
    "Administración": "Administration",
    "Configuración y usuarios": "Configuration et utilisateurs",
    "Ver módulos": "Voir les modules",
    "Bienvenido, {}": "Bienvenue, {}",
    "Selecciona un módulo del menú superior para comenzar": "Sélectionnez un module dans le menu supérieur pour commencer",
    "Utilidades": "Utilitaires",
    "⚙️ Preferencias": "⚙️ Préférences",
    "ℹ️ Acerca de": "ℹ️ À propos",
    "Sesión": "Session",
    "🏢 Cambiar Empresa": "🏢 Changer d'entreprise",
    "🚺 Cerrar Sesión": "🚺 Fermer la session",
    "⚠️ AVISOS": "⚠️ AVIS",
    "✓ Sin Avisos": "✓ Sans avis",
    "No hay avisos pendientes": "Aucun avis en attente",
    "AVISOS": "AVIS",
    "🔄 Limpiar y Refrescar": "🔄 Nettoyer et rafraîchir",
    "Ordenar por:": "Trier par :",
    "Nombre Fiscal": "Nom fiscal",
    "Código": "Code",
    "Fecha": "Date",
    "Modo:": "Mode :",
    "Búsqueda:": "Recherche :",
    "Buscar...": "Rechercher...",
    "➕ Añadir": "➕ Ajouter",
    "📝 Editar": "📝 Modifier",
    "🗑️ Borrar": "🗑️ Supprimer",
    "🛠️ Gestor Módulos": "🛠️ Gestionnaire de modules",
    "📋 Excepciones": "📋 Exceptions",
    "Error al ejecutar": "Erreur lors de l'exécution",
    "No implementado": "Non implémenté",
    "Esta acción aún no está implementada para este módulo": "Cette action n'est pas encore implémentée pour ce module",
    "Refrescar": "Rafraîchir",
    "Actualizando datos de": "Mise à jour des données de",
    "No se pudo encontrar la vista del módulo": "Impossible de trouver la vue du module",
    
    # ========== FORMULARIO CLIENTES ==========
    "Gestion de clientes": "Gestion des clients",
    "Gestión de Clientes - Datos administrativos": "Gestion des clients - Données administratives",
    "Cliente:": "Client :",
    "TextLabel": "Étiquette",
    "Personas de contacto": "Personnes de contact",
    "Otras personas de contacto": "Autres personnes de contact",
    "TIPO CLIENTE": "TYPE DE CLIENT",
    "Editar tipo de cliente": "Modifier le type de client",
    "Tipo": "Type",
    "Nombre": "Nom",
    "Validar VIES": "Valider VIES",
    "Provincia:": "Province :",
    "CP:": "CP :",
    "Mail:": "Mail :",
    "Población:": "Ville :",
    "Móvil:": "Mobile :",
    "Teléfono1:": "Téléphone 1 :",
    "Teléfono 2:": "Téléphone 2 :",
    "Dirección:": "Adresse :",
    "Nombre Comercial:": "Nom commercial :",
    "CIF IVA UE:": "CIF TVA UE :",
    "Pais:": "Pays :",
    "Direccion 2:": "Adresse 2 :",
    "web:": "web :",
    "Nombre Fiscal:": "Nom fiscal :",
    "Código:                        ": "Code :",
    "Observaciones:": "Observations :",
    "Cif/Nif:": "CIF/NIF :",
    "Segundo Apellido:": "Deuxième nom :",
    "Primer Apellido:": "Premier nom :",
    "SIRET": "SIRET",
    "Cliente": "Client",
    "DIRECCIONES": "ADRESSES",
    "Descripción:": "Description :",
    "C.P.": "CP",
    "Población": "Ville",
    "Dirección 2:": "Adresse 2 :",
    "email:": "email :",
    
    # ========== MENSAJES DEL SISTEMA ==========
    "Los datos se han guardado corectamente": "Les données ont été enregistrées correctement",
    "error al guardar datos cliente. Descripción Error: ": "Erreur lors de l'enregistrement des données client. Description de l'erreur : ",
    "No se pudo realizar la transacción, no se guardó la ficha": "La transaction n'a pas pu être effectuée, la fiche n'a pas été enregistrée",
    "Los datos se han guardado corectamente:": "Les données ont été enregistrées correctement :",
    "No existe cliente": "Le client n'existe pas",
    "No existe cliente que coincida con los parámetros de busqueda": "Il n'existe aucun client correspondant aux paramètres de recherche",
    "Añadir deuda cliente": "Ajouter une dette client",
    "Ha fallado la inserción de la deuda en la ficha del paciente": "L'insertion de la dette dans la fiche du patient a échoué",
    "Falló la inserción en la tabla de deudas": "L'insertion dans la table des dettes a échoué",
    "Entregas a cuenta": "Acomptes",
    "No se pudo guardar la entrega": "L'acompte n'a pas pu être enregistré",
    "Modificar deuda Cliente": "Modifier la dette du client",
    "Falló la lectura de la deuda del cliente": "La lecture de la dette du client a échoué",
    "Añadir personas de contacto": "Ajouter des personnes de contact",
    "Falló el añadir una persona de contacto: %1": "L'ajout d'une personne de contact a échoué : %1",
    "editar personas de contacto": "Modifier les personnes de contact",
    "Falló el guardar una persona de contacto: %1": "L'enregistrement d'une personne de contact a échoué : %1",
    "Personas contacto cliente": "Personnes de contact du client",
    "Ocurrió un error al borrar: %1": "Une erreur s'est produite lors de la suppression : %1",
    "Añadir/Guardar dirección": "Ajouter/Enregistrer l'adresse",
    "Ocurrió un error al guardar los datos de dirección: %1": "Une erreur s'est produite lors de l'enregistrement des données d'adresse : %1",
    "Clientes": "Clients",
    "Borrar Ficha": "Supprimer la fiche",
    "Está apunto de borrar la ficha de un cliente\n¿Desea continuar?": "Vous êtes sur le point de supprimer la fiche d'un client\nVoulez-vous continuer ?",
    "No": "Non",
    "Si": "Oui",
    "Borrado corectamente": "Supprimé correctement",
    "Borrar cliente": "Supprimer le client",
    "Falló el borrado del cliente \ndeberá contactar con el administrador para su borrado manual": "La suppression du client a échoué\nvous devez contacter l'administrateur pour une suppression manuelle",
    "Buscar....": "Rechercher....",
    "tabla": "tableau",
    "A-Z": "A-Z",
    "Z-A": "Z-A",
    "Selección": "Sélection",
    "Normativa Pais": "Réglementation du pays",
    "Francia": "France",
    "España": "Espagne",
    
    # ========== MÓDULOS (para botones) ==========
    "Clientes": "Clients",
    "Empresas": "Entreprises",
    "Gestor de Módulos": "Gestionnaire de modules",
    
    # ========== ACCIONES DE MÓDULOS ==========
    "Nueva": "Nouvelle",
    "Crear nueva factura": "Créer une nouvelle facture",
    "Buscar facturas": "Rechercher des factures",
    "Ver listado completo": "Voir la liste complète",
    "Imprimir": "Imprimer",
    "Imprimir factura": "Imprimer la facture",
    "Exportar": "Exporter",
    "Exportar XML/PDF": "Exporter XML/PDF",
    "Nuevo": "Nouveau",
    "Crear nuevo cliente": "Créer un nouveau client",
    "Buscar clientes": "Rechercher des clients",
    "Ver todos los clientes": "Voir tous les clients",
    "Estadísticas": "Statistiques",
    "Estadísticas de clientes": "Statistiques clients",
    "Crear nuevo producto": "Créer un nouveau produit",
    "Buscar productos": "Rechercher des produits",
    "Inventario": "Inventaire",
    "Ver inventario": "Voir l'inventaire",
    "Categorías": "Catégories",
    "Gestionar categorías": "Gérer les catégories",
    "Crear nuevo proyecto": "Créer un nouveau projet",
    "Dashboard": "Tableau de bord",
    "Panel de proyectos": "Tableau de bord des projets",
    "Planificación": "Planification",
    "Planificar tareas": "Planifier les tâches",
    "Presupuestos": "Budgets",
    "Gestionar presupuestos": "Gérer les budgets",
    
    # ========== NOMBRES DE MÓDULOS (Contexto Modules) ==========
    "Clientes": "Clients",
    "Presupuestos": "Budgets",
    "Albaranes": "Bons de livraison",
    "Facturas": "Factures",
    "Proveedores": "Fournisseurs",
    "Facturas de Compra": "Factures d'achat",
    "Artículos": "Articles",
    "Almacén": "Entrepôt",
    "Contabilidad": "Comptabilité",
    "Tesorería": "Trésorerie",
    "Proyectos": "Projets",
    "Control de Tiempo": "Suivi du temps",
    "Empresas": "Entreprises",
    "Usuarios": "Utilisateurs",
    "Configuración": "Configuration",
    "Informes": "Rapports",
    "Gestor Módulos": "Gestionnaire de modules",
    
    # Descripciones de módulos
    "Gestión de clientes y contactos": "Gestion des clients et contacts",
    "Creación de presupuestos": "Création de budgets",
    "Albaranes de entrega": "Bons de livraison",
    "Emisión y gestión de facturas": "Émission et gestion des factures",
    "Gestión de proveedores": "Gestion des fournisseurs",
    "Registro de facturas de proveedores": "Enregistrement des factures fournisseurs",
    "Catálogo de productos y servicios": "Catalogue de produits et services",
    "Control de inventario y stock": "Contrôle d'inventaire et de stock",
    "Asientos contables y balance": "Écritures comptables et bilan",
    "Gestión de cobros y pagos": "Gestion des encaissements et paiements",
    "Gestión de proyectos creativos": "Gestion de projets créatifs",
    "Registro de horas trabajadas": "Enregistrement des heures travaillées",
    "Gestión de empresas y multi-empresa": "Gestion des entreprises et multi-entreprise",
    "Gestión de usuarios y permisos": "Gestion des utilisateurs et permissions",
    "Configuración general del sistema": "Configuration générale du système",
    "Informes y estadísticas": "Rapports et statistiques",
    "Ver módulos y otorgar permisos por rol": "Voir les modules et attribuer des permissions par rôle",
    
    # ========== BARRA DE ESTADO Y ROLES ==========
    "Administrador": "Administrateur",
    "Gerente": "Gérant",
    "Contable": "Comptable",
    # "Ventas": "Ventes", # Ya existe
    "Jefe de Proyecto": "Chef de projet",
    "Empleado": "Employé",
    "Visor": "Spectateur",
    "Usuario": "Utilisateur",
    "Rol": "Rôle",
    "Normativa": "Réglementation",
    "Francia": "France",
    "España": "Espagne",
    "Módulo {} activo": "Module {} actif",
    "Módulo {} cargado": "Module {} chargé",
    
    # ========== VISTA DE CLIENTES (TABLA) ==========
    "📋 Gestión de Clientes": "📋 Gestion des Clients",
    "Buscar:": "Rechercher :",
    "Nombre, CIF, teléfono...": "Nom, NIF, téléphone...",
    "ID": "ID",
    "Código": "Code",
    "Nombre Fiscal": "Raison Sociale",
    "CIF/NIF": "NIF/TVA",
    "NIF/CIF": "NIF/TVA",
    "Teléfono": "Téléphone",
    "Email": "E-mail",
    "Población": "Ville",
    "0 clientes": "0 clients",
    "{} clientes": "{} clients",
    "{} de {} clientes": "{} sur {} clients",
    "Editar Cliente": "Modifier Client",
    "Editar cliente #{}: {}\n\nEl formulario de edición completo se implementará próximamente.": "Modifier le client #{}: {}\n\nLe formulaire d'édition complet sera bientôt disponible.",
    "Nuevo Cliente": "Nouveau Client",
    "El formulario de creación de clientes se implementará próximamente.": "Le formulaire de création de clients sera bientôt disponible.",
    "Atención": "Attention",
    "Selecciona un cliente primero.": "Veuillez sélectionner un client d'abord.",
    "Confirmar eliminación": "Confirmer la suppression",
    "¿Seguro que deseas eliminar al cliente #{}: {}?": "Êtes-vous sûr de vouloir supprimer le client #{}: {} ?",
    "Éxito": "Succès",
    "Cliente eliminado correctamente.": "Client supprimé avec succès.",
    
    # ========== MENSAJES DE VALIDACIÓN (ClientesViewFull) ==========
    "El código de cliente es obligatorio.": "Le code client est obligatoire.",
    "Debe introducir el nombre o el nombre fiscal del cliente.": "Vous devez saisir le nom ou la raison sociale du client.",
    "El NIF/CIF introducido no parece válido.": "Le NIF/TVA saisi ne semble pas valide.",
    "El email introducido no es válido.": "L'e-mail saisi n'est pas valide.",
    "La cuenta bancaria (CCC) no es válida.": "Le compte bancaire (CCC) n'est pas valide.",
    "El IBAN introducido no es válido.": "L'IBAN saisi n'est pas valide.",
    "Día de pago {} fuera de rango 0-31.": "Jour de paiement {} hors de la plage 0-31.",
    "Día de pago {} no es un número válido.": "Le jour de paiement {} n'est pas un nombre valide.",
    
    # ========== MENSAJES DE DIÁLOGO (ClientesViewFull) ==========
    "Error": "Erreur",
    "Error al cargar clientes: {}": "Erreur lors du chargement des clients : {}",
    "Error al filtrar clientes: {}": "Erreur lors du filtrage des clients : {}",
    "No se pudo cargar el cliente": "Impossible de charger le client",
    "Aviso": "Avertissement",
    "Seleccione un cliente para editar": "Sélectionnez un client à modifier",
    "Seleccione un cliente para borrar": "Sélectionnez un client à supprimer",
    "Confirmar borrado": "Confirmer la suppression",
    "¿Está seguro de que desea borrar el cliente '{}'?": "Êtes-vous sûr de vouloir supprimer le client '{}' ?",
    "Cliente borrado correctamente": "Client supprimé avec succès",
    "No se puede borrar": "Impossible de supprimer",
    "Error al borrar: {}": "Erreur lors de la suppression : {}",
    "Validación": "Validation",
    "Cliente creado": "Client créé",
    "Error al guardar: {}": "Erreur lors de l'enregistrement : {}",
}

def translate_ts_file(ts_file_path):
    """Traduce todas las cadenas del archivo .ts al francés"""
    tree = ET.parse(ts_file_path)
    root = tree.getroot()
    
    count = 0
    total = 0
    
    for message in root.findall('.//message'):
        source = message.find('source')
        translation = message.find('translation')
        
        if source is not None and translation is not None:
            source_text = source.text or ''
            total += 1
            
            if source_text in translations:
                translation.text = translations[source_text]
                if 'type' in translation.attrib:
                    del translation.attrib['type']
                count += 1
    
    tree.write(ts_file_path, encoding='utf-8', xml_declaration=True)
    
    print(f"✅ Traducidas {count} de {total} cadenas al francés")
    print(f"⚠️  Quedan {total - count} cadenas sin traducir")
    
    return count, total

if __name__ == "__main__":
    import sys
    ts_file = sys.argv[1] if len(sys.argv) > 1 else 'translations/creative_erp_fr.ts'
    translate_ts_file(ts_file)
