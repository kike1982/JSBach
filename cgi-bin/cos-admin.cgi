#!/bin/bash

# cos-admin.cgi - Consola de Gestión Rediseñada

source /usr/local/JSBach/conf/variables.conf
source $DIR/$PROJECTE/$DIR_CONF/$CONF_IFWAN

echo "Content-type: text/html; charset=utf-8"
echo ""

# Obtener información del sistema
UPTIME=$(uptime -p | sed 's/up //')
SYS_TIME=$(date +"%H:%M:%S")
SYS_DATE=$(date +"%d/%m/%Y")

# Intentar obtener IP de gestión (br0 preferido, luego WAN)
IP_GESTIO=$(ip -4 addr show dev br0 2>/dev/null | grep -oP '(?<=inet\s)\d+(\.\d+){3}' | head -n1)
if [ -z "$IP_GESTIO" ]; then
    IP_GESTIO=$(ip -4 addr show dev "$IFW_IFWAN" 2>/dev/null | grep -oP '(?<=inet\s)\d+(\.\d+){3}' | head -n1)
fi
[ -z "$IP_GESTIO" ] && IP_GESTIO="No asignada"

cat <<EOF
<!DOCTYPE html>
<html lang="es">
<head>
    <link rel="stylesheet" href="/cgi-bin/style.cgi">
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Consola de Gestión JSBach</title>
</head>
<body>
    <div class="header-panel">
        <h1>Consola de Gestión JSBach</h1>
        <div class="system-info">
            <div class="info-item">
                <span class="info-label">Hora del Sistema</span>
                <span class="info-value">$SYS_TIME</span>
            </div>
            <div class="info-item">
                <span class="info-label">Fecha</span>
                <span class="info-value">$SYS_DATE</span>
            </div>
            <div class="info-item">
                <span class="info-label">Tiempo Activo</span>
                <span class="info-value">$UPTIME</span>
            </div>  
        </div>
    </div>

    <!-- El resto del contenido (módulos) ha sido movido a la página de información -->
</body>
</html>
EOF
