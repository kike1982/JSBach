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
    <link rel="stylesheet" href="/cgi-bin/style.cgi">
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Información del Sistema - JSBach</title>
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
