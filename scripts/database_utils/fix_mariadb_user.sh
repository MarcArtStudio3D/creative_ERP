#!/bin/bash
# Script para verificar y arreglar el usuario admin de MariaDB

echo "======================================================================"
echo "VERIFICACIÓN Y CORRECCIÓN DEL USUARIO ADMIN"
echo "======================================================================"
echo ""

echo "1️⃣ Verificando usuarios existentes..."
sudo mariadb -e "SELECT User, Host, plugin, authentication_string FROM mysql.user WHERE User IN ('root', 'admin');"

echo ""
echo "2️⃣ Eliminando usuarios admin existentes (si los hay)..."
sudo mariadb -e "DROP USER IF EXISTS 'admin'@'localhost';"
sudo mariadb -e "DROP USER IF EXISTS 'admin'@'127.0.0.1';"
sudo mariadb -e "DROP USER IF EXISTS 'admin'@'%';"

echo ""
echo "3️⃣ Creando usuario admin con contraseña..."
sudo mariadb -e "
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin123';
CREATE USER 'admin'@'127.0.0.1' IDENTIFIED BY 'admin123';
CREATE USER 'admin'@'%' IDENTIFIED BY 'admin123';
"

echo ""
echo "4️⃣ Otorgando permisos completos..."
sudo mariadb -e "
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'127.0.0.1' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
"

echo ""
echo "5️⃣ Verificando usuarios después de la creación..."
sudo mariadb -e "SELECT User, Host, plugin FROM mysql.user WHERE User = 'admin';"

echo ""
echo "6️⃣ Probando conexión con el nuevo usuario..."
if mariadb -h 127.0.0.1 -u admin -padmin123 -e "SELECT 'Conexión exitosa' AS status;" 2>/dev/null; then
    echo "✅ ¡Conexión exitosa con usuario admin!"
    echo ""
    echo "Connection details for Antares/DBeaver:"
    echo "   Host: 127.0.0.1"
    echo "   Puerto: 3306"
    echo "   Usuario: admin"
    echo "   Contraseña: admin123"
    echo "   Base de datos: creative_erp"
else
    echo "❌ No se pudo conectar con el usuario admin"
    echo ""
    echo "Verificando configuración de MariaDB..."
    echo ""
    echo "Verificando bind-address en configuración:"
    sudo grep -r "bind-address" /etc/mysql/ 2>/dev/null | grep -v "#"
    echo ""
    echo "Note: If bind-address is set to 127.0.0.1 or 0.0.0.0, that's fine."
    echo "   Si no aparece nada, también está bien (usa el valor por defecto)."
fi

echo ""
echo "======================================================================"
