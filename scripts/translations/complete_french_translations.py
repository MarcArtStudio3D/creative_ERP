#!/usr/bin/env python3
"""
Script para completar TODAS las traducciones faltantes en creative_erp_fr.ts
"""

import re
from pathlib import Path

# Diccionario completo de traducciones adicionales
ADDITIONAL_TRANSLATIONS = {
    "0,00": "0,00",
    "Abril:": "Avril :",
    "Activar Bloqueo cliente": "Activer le blocage client",
    "Agente: ": "Agent : ",
    "Agosto:": "Août :",
    "Albaranes": "Bons de livraison",
    "año/cad": "année/exp",
    "Asientos Contables": "Écritures comptables",
    "Cliente Empresa (Aplicar IRPF)": "Client entreprise (Appliquer retenue)",
    "Cobro ": "Encaissement ",
    "codigo": "code",
    "Comentarios generales sobre el cliente:": "Commentaires généraux sur le client :",
    "Comentarios y Otros": "Commentaires et autres",
    "Cuenta": "Compte",
    "Cuenta Cobros:": "Compte encaissements :",
    "Cuenta contable:": "Compte comptable :",
    "Cuenta deudas:": "Compte dettes :",
    "Cuenta IVA Repercutido:": "Compte TVA collectée :",
    "Cuenta Valida": "Compte valide",
    "D.C.:": "D.C. :",
    "dd/MM/yyyy": "dd/MM/yyyy",
    "Deuda Actual:": "Dette actuelle :",
    "Deudas": "Dettes",
    "Diciembre:": "Décembre :",
    "Enero:": "Janvier :",
    "Entidad:": "Entité :",
    "Entregado a cuenta:": "Acompte versé :",
    "Estadistica": "Statistiques",
    "Exento": "Exonéré",
    "Exportación": "Exportation",
    "Febrero:": "Février :",
    "Fecha de Alta:": "Date d'inscription :",
    "Fecha Nacimiento:": "Date de naissance :",
    "Fecha ultima compra:": "Date dernier achat :",
    "General": "Général",
    "Gestión de Pacientes - Datos administrativos": "Gestion des patients - Données administratives",
    "Gestión deuda cliente": "Gestion dette client",
    "Historial": "Historique",
    "Historial de deuda": "Historique de dette",
    "Hora:": "Heure :",
    "idioma Documentos:": "Langue documents :",
    "Importe Acumulado:": "Montant cumulé :",
    "Importe Vales:": "Montant bons :",
    "Iva Cliente": "TVA client",
    "Julio:": "Juillet :",
    "Junio:": "Juin :",
    "&lt;html&gt;&lt;head/&gt;&lt;body&gt;&lt;p&gt;&lt;span style=&quot; font-size:11pt; text-decoration: underline; color:#ff0000;&quot;&gt;Contabilidad (P.G.C):&lt;/span&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;": "&lt;html&gt;&lt;head/&gt;&lt;body&gt;&lt;p&gt;&lt;span style=&quot; font-size:11pt; text-decoration: underline; color:#ff0000;&quot;&gt;Comptabilité (P.C.G.) :&lt;/span&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;",
    "&lt;html&gt;&lt;head/&gt;&lt;body&gt;&lt;p&gt;&lt;span style=&quot; font-size:11pt; text-decoration: underline; color:#ff0000;&quot;&gt;Datos financieros:&lt;/span&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;": "&lt;html&gt;&lt;head/&gt;&lt;body&gt;&lt;p&gt;&lt;span style=&quot; font-size:11pt; text-decoration: underline; color:#ff0000;&quot;&gt;Données financières :&lt;/span&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;",
    "Marzo": "Mars",
    "Mayo:": "Mai :",
    "mes/cad": "mois/exp",
    "Noviembre:": "Novembre :",
    "Octubre:": "Octobre :",
    "Oficina:": "Bureau :",
    "Pagadas": "Payées",
    "Password Acceso web:": "Mot de passe accès web :",
    "Pedidos": "Commandes",
    "Pendientes": "En attente",
    "Presupuestos": "Devis",
    "Recargo Equivalencia": "Majoration équivalence",
    "Riesgo permitido:": "Risque autorisé :",
    "Septiembre:": "Septembre :",
    "tarjeta": "carte",
    "Tipo de aviso:": "Type d'avis :",
    "Transportista:": "Transporteur :",
    "U.E.": "U.E.",
    "Usuario Acceso Web:": "Utilisateur accès web :",
    "Ventas Ejercicio:": "Ventes exercice :",
    "Ver Asientos Cliente": "Voir écritures client",
    "Visa1 distancia:": "Visa1 distance :",
    "Visa2_distancia:": "Visa2 distance :",
    "C.P.": "Code postal :",
}


def translate_remaining(input_file: Path):
    """Traduce los strings restantes."""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    translations_count = 0
    
    # Buscar todos los bloques <message> con translation unfinished
    pattern = r'(<message>.*?<source>(.*?)</source>.*?<translation type="unfinished"></translation>.*?</message>)'
    
    def replace_translation(match):
        nonlocal translations_count
        full_block = match.group(1)
        source_text = match.group(2)
        
        # Buscar traducción
        if source_text in ADDITIONAL_TRANSLATIONS:
            translation = ADDITIONAL_TRANSLATIONS[source_text]
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
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return translations_count


def main():
    input_file = Path("translations/creative_erp_fr.ts")
    
    print("=" * 60)
    print("Completando traducciones restantes al francés")
    print("=" * 60)
    
    count = translate_remaining(input_file)
    
    print(f"\n✓ {count} traducciones adicionales aplicadas")
    print(f"✓ Archivo actualizado: {input_file}")
    
    # Verificar cuántas quedan
    import subprocess
    result = subprocess.run(
        ["grep", "-c", 'type="unfinished"', str(input_file)],
        capture_output=True,
        text=True
    )
    
    remaining = int(result.stdout.strip()) if result.returncode == 0 else 0
    print(f"\n📊 Strings sin traducir restantes: {remaining}")
    
    if remaining == 0:
        print("\n🎉 ¡Todas las traducciones completadas!")
    
    print("\nPróximo paso:")
    print("  python scripts/compile_translations.py")
    print()


if __name__ == "__main__":
    main()
