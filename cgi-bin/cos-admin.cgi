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
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Consola de Gestión JSBach</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #3b82f6;
            --primary-hover: #2563eb;
            --bg: #0f172a;
            --card-bg: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border: rgba(255,255,255,0.1);
            --accent: #1e293b;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            margin: 0;
            padding: 1.5rem;
        }

        .header-panel {
            background: var(--accent);
            color: white;
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.3);
            border: 1px solid var(--border);
        }

        .header-panel h1 {
            margin: 0;
            font-size: 1.5rem;
            font-weight: 600;
            letter-spacing: -0.025em;
        }

        .system-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1.5rem;
            margin-top: 1.5rem;
            padding-top: 1.5rem;
            border-top: 1px solid rgba(255,255,255,0.1);
        }

        .info-item {
            display: flex;
            flex-direction: column;
        }

        .info-label {
            font-size: 0.75rem;
            color: rgba(255,255,255,0.6);
            text-transform: uppercase;
            font-weight: 600;
        }

        .info-value {
            font-size: 1rem;
            font-weight: 500;
        }

        .grid-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
        }

        .module-card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .module-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
        }

        .module-card h2 {
            margin: 0 0 0.5rem 0;
            font-size: 1.125rem;
            color: var(--primary);
        }

        .module-card p {
            font-size: 0.875rem;
            color: var(--text-muted);
            margin-bottom: 1.5rem;
        }

        .btn-view {
            background-color: var(--primary);
            color: white;
            border: none;
            padding: 0.75rem;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
            width: 100%;
            text-align: center;
            text-decoration: none;
            font-size: 0.875rem;
        }

        .btn-view:hover {
            background-color: var(--primary-hover);
        }
    </style>
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
