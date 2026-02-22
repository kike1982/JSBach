#!/bin/bash

# info.cgi - Rediseñado con estilo profesional, colores y emoticonos

source /usr/local/JSBach/conf/variables.conf

# Función para obtener el estado de un módulo
get_status() {
    local mod=$1
    local res=""
    case "$mod" in
        wan)
            if /usr/local/JSBach/scripts/client_srv_cli ifwan estat | grep -qw "ACTIVAT"; then
                res="ACTIVAT"
            else
                res="DESACTIVAT"
            fi
            ;;
        enrutar)
            if /usr/local/JSBach/scripts/client_srv_cli enrutar estat | grep -qw "ACTIVAT"; then
                res="ACTIVAT"
            else
                res="DESACTIVAT"
            fi
            ;;
        bridge)
            if /usr/local/JSBach/scripts/client_srv_cli bridge estat | grep -qw "ACTIVAT"; then
                res="ACTIVAT"
            else
                res="DESACTIVAT"
            fi
            ;;
        tallafocs)
            # Aislamos solo la tabla filter (antes de "📊 NAT") para evitar falsos positivos con enrutamiento
            if /usr/local/JSBach/scripts/client_srv_cli tallafocs estat | sed '/📊 NAT/,$d' | grep -v "📊" | grep -v "Chain" | grep -v "policy" | grep -v "num" | grep -v "pkts" | grep -v "^$" | grep -q "."; then
                res="ACTIVAT"
            else
                res="DESACTIVAT"
            fi
            ;;
        dmz)
            if /usr/local/JSBach/scripts/client_srv_cli dmz estat | grep -qw "ACTIVAT"; then
                res="ACTIVAT"
            else
                res="DESACTIVAT"
            fi
            ;;
        switch)
            # Check if any switch is active
            if /usr/local/JSBach/scripts/client_srv_cli switch estat | grep -qw "ACTIVAT"; then
                res="ACTIVAT"
            else
                res="DESACTIVAT"
            fi
            ;;
    esac
    echo "$res"
}

# --- Manejador AJAX ---
ACTION=$(echo "$QUERY_STRING" | sed -n 's/.*action=\([^&]*\).*/\1/p')
MOD_REQ=$(echo "$QUERY_STRING" | sed -n 's/.*mod=\([^&]*\).*/\1/p')

if [ "$ACTION" == "status" ] && [ -n "$MOD_REQ" ]; then
    echo "Content-type: text/plain"
    echo ""
    get_status "$MOD_REQ"
    exit 0
fi

echo "Content-type: text/html; charset=utf-8"
echo ""

MODULO=$(echo "$QUERY_STRING" | sed -n 's/.*modulo=\([^&]*\).*/\1/p')

# --- Generar HTML ---
cat <<EOF
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Información del Sistema - JSBach</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #3b82f6;
            --success: #10b981;
            --danger: #ef4444;
            --bg: #0f172a;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border: rgba(255,255,255,0.1);
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            margin: 0;
            padding: 2rem;
            line-height: 1.5;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 2rem;
            align-items: start;
        }

        h1 {
            grid-column: 1 / -1;
            font-size: 2.25rem;
            font-weight: 600;
            margin-bottom: 3rem;
            color: #f8fafc;
            text-align: center;
            letter-spacing: -0.025em;
        }

        .card {
            background: #1e293b;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.3), 0 2px 4px -1px rgba(0,0,0,0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            display: flex;
            flex-direction: column;
            border: 1px solid var(--border);
        }

        .card:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 25px -5px rgba(0,0,0,0.4), 0 10px 10px -5px rgba(0,0,0,0.2);
        }

        /* Colores temáticos por módulo (más oscuros para dark mode) */
        .card-wan { background: linear-gradient(135deg, #1e293b 0%, #1e3a8a 100%); border-left: 5px solid #3b82f6; }
        .card-enrutar { background: linear-gradient(135deg, #1e293b 0%, #064e3b 100%); border-left: 5px solid #10b981; }
        .card-bridge { background: linear-gradient(135deg, #1e293b 0%, #713f12 100%); border-left: 5px solid #eab308; }
        .card-tallafocs { background: linear-gradient(135deg, #1e293b 0%, #7f1d1d 100%); border-left: 5px solid #ef4444; }
        .card-dmz { background: linear-gradient(135deg, #1e293b 0%, #4c1d95 100%); border-left: 5px solid #a855f7; }
        .card-switch { background: linear-gradient(135deg, #1e293b 0%, #a16207 100%); border-left: 5px solid #eab308; }

        .card-header {
            padding: 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .card-title {
            font-size: 1.25rem;
            font-weight: 700;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            color: #f8fafc;
        }

        .status-badge {
            padding: 0.35rem 0.85rem;
            border-radius: 9999px;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .status-active { background-color: #059669; color: white; }
        .status-inactive { background-color: #475569; color: white; }

        details {
            border-top: 1px solid rgba(255,255,255,0.1);
        }

        summary {
            padding: 1rem 1.5rem;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.9rem;
            color: #94a3b8;
            list-style: none;
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: rgba(255,255,255,0.05);
            transition: background 0.2s;
        }

        summary:hover {
            background: rgba(255,255,255,0.1);
        }

        summary::after {
            content: '↓';
            font-weight: bold;
            transition: transform 0.3s;
        }

        details[open] summary::after {
            transform: rotate(180deg);
        }

        .info-content {
            padding: 1.5rem;
            background: rgba(15, 23, 42, 0.6);
            font-size: 0.95rem;
            color: #cbd5e1;
            border-bottom-left-radius: 16px;
            border-bottom-right-radius: 16px;
        }

        ul {
            padding-left: 1.25rem;
            margin: 0.5rem 0 0 0;
        }

        li {
            margin-bottom: 0.5rem;
        }

        .no-selection {
            grid-column: 1 / -1;
            text-align: center;
            padding: 4rem;
            background: #1e293b;
            border-radius: 20px;
            border: 2px dashed rgba(255,255,255,0.1);
            color: var(--text-muted);
        }

        code {
            background: rgba(255,255,255,0.1);
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            font-family: ui-monospace, monospace;
            font-size: 0.85rem;
            color: #e2e8f0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Centro de Control JSBach</h1>
EOF

# --- Helper to render module card ---
render_card() {
    local id=$1
    local title=$2
    local icon=$3
    local class=$4
    local content=$5
    # El estado inicial es "Cargando..." para que la página sea instantánea
    local status="Cargando..."
    local status_class="status-inactive"

    cat <<EOF
    <div class="card $class" id="card-$id">
        <div class="card-header">
            <h2 class="card-title"><span>$icon</span> $title</h2>
            <span id="status-$id" class="status-badge $status_class">$status</span>
        </div>
        <details>
            <summary>Detalles Técnicos</summary>
            <div class="info-content">
                $content
            </div>
        </details>
    </div>
EOF
}

# --- AJAX Status Loader ---
cat <<EOF
<script>
document.addEventListener('DOMContentLoaded', () => {
    // Lista de módulos a consultar de forma asíncrona
    const modules = ['wan', 'enrutar', 'bridge', 'tallafocs', 'dmz', 'switch'];
    
    modules.forEach(mod => {
        const badge = document.getElementById('status-' + mod);
        if (!badge) return;
        
        // Consultar el estado real al servidor sin bloquear la carga de la página
        fetch('info.cgi?action=status&mod=' + mod)
            .then(response => response.text())
            .then(status => {
                status = status.trim();
                badge.textContent = status || 'DESCONOCIDO';
                
                if (status === 'ACTIVAT') {
                    badge.classList.remove('status-inactive');
                    badge.classList.add('status-active');
                } else {
                    badge.classList.remove('status-active');
                    badge.classList.add('status-inactive');
                }
            })
            .catch(err => {
                console.error('Error al cargar estado de ' + mod, err);
                badge.textContent = 'ERROR';
            });
    });
});
</script>
EOF

# --- Contenido de los módulos ---
CONTENT_WAN="
<p>Gestiona la conexión principal a Internet:</p>
<ul>
    <li>Compatible con <strong>DHCP</strong> o IP <strong>Estática</strong>.</li>
    <li>Asegura la conectividad DNS del sistema.</li>
    <li>Puerta de enlace predeterminada automática.</li>
</ul>"

CONTENT_ENRUTAR="
<p>Administra el tráfico entre redes:</p>
<ul>
    <li>Activa el <strong>IP Forwarding</strong> en el kernel.</li>
    <li>Reglas de NAT (Network Address Translation).</li>
    <li>Permite que los clientes accedan al exterior.</li>
</ul>"

CONTENT_BRIDGE="
<p>Controla las interfaces en modo puente:</p>
<ul>
    <li>Segmentación avanzada mediante <strong>VLANs</strong>.</li>
    <li>Filtrado de tráfico a nivel de enlace (Capa 2).</li>
    <li>Aislamiento de clientes en el mismo segmento.</li>
</ul>"

CONTENT_TALLAFOCS="
<p>Protección perimetral del sistema:</p>
<ul>
    <li>Filtrado de paquetes mediante <strong>Iptables</strong>.</li>
    <li>Control de acceso granular por subred.</li>
    <li>Protección contra escaneos y ataques externos.</li>
</ul>"

CONTENT_DMZ="
<p>Exposición segura de servicios:</p>
<ul>
    <li>Redireccionamiento de puertos (DNAT).</li>
    <li>Soporte para servidores web, juegos, etc.</li>
    <li>Protege la red interna de intrusiones.</li>
</ul>"

CONTENT_SWITCH="
<p>Gestión de dispositivos de red (Switches):</p>
<ul>
    <li>Monitorización de estado y conectividad.</li>
    <li>Visualización de tablas de MACs.</li>
    <li>Gestión de Listas de Control de Acceso (ACLs).</li>
</ul>"

# --- Mostrar módulos ---
if [ -z "$MODULO" ]; then
    # Por defecto mostrar todos
    render_card "wan" "WAN" "🌐" "card-wan" "$CONTENT_WAN"
    render_card "enrutar" "Enrutar" "⚡" "card-enrutar" "$CONTENT_ENRUTAR"
    render_card "bridge" "Bridge" "🌉" "card-bridge" "$CONTENT_BRIDGE"
    render_card "tallafocs" "Tallafocs" "🔥" "card-tallafocs" "$CONTENT_TALLAFOCS"
    render_card "dmz" "DMZ" "🛡️" "card-dmz" "$CONTENT_DMZ"
    render_card "switch" "Switches" "🔌" "card-switch" "$CONTENT_SWITCH"
else
    case "$MODULO" in
        wan) render_card "wan" "WAN" "🌐" "card-wan" "$CONTENT_WAN" ;;
        enrutar) render_card "enrutar" "Enrutar" "⚡" "card-enrutar" "$CONTENT_ENRUTAR" ;;
        bridge) render_card "bridge" "Bridge" "🌉" "card-bridge" "$CONTENT_BRIDGE" ;;
        tallafocs) render_card "tallafocs" "Tallafocs" "🔥" "card-tallafocs" "$CONTENT_TALLAFOCS" ;;
        dmz) render_card "dmz" "DMZ" "🛡️" "card-dmz" "$CONTENT_DMZ" ;;
        switch) render_card "switch" "Switches" "🔌" "card-switch" "$CONTENT_SWITCH" ;;
        *) echo "<div class='no-selection'>⚠️ Módulo <code>$MODULO</code> no encontrado.</div>" ;;
    esac
fi

cat <<EOF
    </div>
</body>
</html>
EOF
