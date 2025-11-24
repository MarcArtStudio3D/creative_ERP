#!/bin/bash
# Script para verificar el estado de MariaDB y crear usuario si es necesario

echo "======================================================================"
echo "DIAGNÓSTICO Y CONFIGURACIÓN DE MARIADB"
echo "======================================================================"
echo ""

# Verificar usuarios actuales
echo "1️⃣ Verificando usuarios de MariaDB..."
sudo mariadb -e "SELECT User, Host, plugin FROM mysql.user WHERE User IN ('root', 'admin', 'marc');" 2>/dev/null

if [ $? -eq 0 ]; then
    echo ""
    echo "2️⃣ Verificando bases de datos..."
    sudo mariadb -e "SHOW DATABASES LIKE 'creative_erp';" 2>/dev/null
    
    echo ""
    echo "3️⃣ Verificando tablas en creative_erp..."
    sudo mariadb creative_erp -e "SHOW TABLES;" 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "4️⃣ Contando registros en cada tabla..."
        sudo mariadb creative_erp -e "
            SELECT 
                table_name,
                table_rows
            FROM information_schema.tables
            WHERE table_schema = 'creative_erp'
            ORDER BY table_name;
        " 2>/dev/null
        
        echo ""
        echo "======================================================================"
        echo "✅ Las tablas EXISTEN en MariaDB local"
        echo "======================================================================"
        echo ""
        echo "💡 PROBLEMA: El usuario 'root' usa autenticación por socket Unix"
        echo "   No puedes conectarte con contraseña desde aplicaciones externas."
        echo ""
        echo "🔧 SOLUCIÓN: Crear un nuevo usuario con autenticación por contraseña"
        echo ""
        read -p "¿Quieres crear un usuario 'admin' con contraseña 'admin123'? (s/n): " respuesta
        
        if [ "$respuesta" = "s" ] || [ "$respuesta" = "S" ]; then
            echo ""
            echo "Creando usuario 'admin'..."
            sudo mariadb -e "
                CREATE USER IF NOT EXISTS 'admin'@'localhost' IDENTIFIED BY 'admin123';
                CREATE USER IF NOT EXISTS 'admin'@'127.0.0.1' IDENTIFIED BY 'admin123';
                GRANT ALL PRIVILEGES ON creative_erp.* TO 'admin'@'localhost';
                GRANT ALL PRIVILEGES ON creative_erp.* TO 'admin'@'127.0.0.1';
                FLUSH PRIVILEGES;
            "
            
            if [ $? -eq 0 ]; then
                echo "✅ Usuario 'admin' creado exitosamente"
                echo ""
                echo "📋 Usa estos datos para conectarte con Antares/DBeaver:"
                echo "   Host: 127.0.0.1"
                echo "   Puerto: 3306"
                echo "   Usuario: admin"
                echo "   Contraseña: admin123"
                echo "   Base de datos: creative_erp"
            else
                echo "❌ Error al crear usuario"
            fi
        fi
    else
        echo "⚠️  La base de datos 'creative_erp' existe pero está vacía"
    fi
else
    echo "❌ No se pudo conectar a MariaDB"
    echo "   Necesitas permisos de sudo para ejecutar este script"
fi

echo ""
echo "======================================================================"
