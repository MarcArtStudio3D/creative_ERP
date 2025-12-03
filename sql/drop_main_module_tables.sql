-- WARNING: destructive SQL. Run only after you have backups and are sure.
-- Generated template for dropping module tables from `creative_erp_main`.

DROP TABLE IF EXISTS `articulos`;
DROP TABLE IF EXISTS `articulos_imagenes`;
DROP TABLE IF EXISTS `articulos_ofertas`;
DROP TABLE IF EXISTS `clientes`;
DROP TABLE IF EXISTS `familias`;
DROP TABLE IF EXISTS `subfamilias`;
DROP TABLE IF EXISTS `tarifas`;
DROP TABLE IF EXISTS `kits`;
DROP TABLE IF EXISTS `proveedores_frecuentes`;
DROP TABLE IF EXISTS `direcciones_alternativas`;
DROP TABLE IF EXISTS `deudas_clientes`;
DROP TABLE IF EXISTS `estadisticas_clientes_mes`;
DROP TABLE IF EXISTS `historial_clientes`;
-- Correct table names (tipocliente_def and tiposubcliente_def)
DROP TABLE IF EXISTS `tipocliente_def`;
DROP TABLE IF EXISTS `tiposubcliente_def`;


-- Keep core Alembic and global tables (alembic_version, users, empresas, etc.) unless you specifically want to remove them.
