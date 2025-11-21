# Archivos fuente Python
SOURCES = app/app.py \
          app/views/login_window_multi.py \
          app/views/main_window_v2.py \
          app/views/ui_db_consulta_view.py \
          app/views/ui_frmeditaravisos.py \
          app/views/ui_frmempresas.py \
          app/views/ui_frmnuevosavisos.py \
          core/auth.py \
          core/business.py \
          core/db.py \
          core/invoices.py \
          core/models.py \
          core/modules.py \
          core/repositories.py \
          modules/clientes/view.py \
          modules/clientes/view_full.py \
          modules/empresas/view.py \
          modules/gestor_modulos/view.py \
          main.py

# Archivos de interfaz de Qt Designer
FORMS = app/ui/db_consulta_view.ui \
        app/ui/frmClientes.ui \
        app/ui/frmeditaravisos.ui \
        app/ui/frmempresas.ui \
        app/ui/frmnuevosavisos.ui

# Archivos de traducción
TRANSLATIONS = translations/creative_erp_es.ts \
               translations/creative_erp_en.ts \
               translations/creative_erp_ca.ts \
               translations/creative_erp_fr.ts
