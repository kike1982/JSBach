#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

/bin/cat <<'EOM'
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Gestió WAN</title>
    <style>
        body {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background: #0f172a;
            margin: 24px;
            color: #f8fafc;
            line-height: 1.5;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        .card {
            background: #1e293b;
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        }
        .card-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 16px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            padding-bottom: 12px;
        }
        .card-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: #3b82f6;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .badge {
            font-size: 0.75rem;
            font-weight: 800;
            padding: 4px 12px;
            border-radius: 9999px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .badge-manual { background: rgba(59, 130, 246, 0.2); color: #60a5fa; border: 1px solid rgba(96, 165, 250, 0.3); }
        .badge-dhcp { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(52, 211, 153, 0.3); }
        .output-box {
            background: #0f172a;
            border-radius: 8px;
            padding: 16px;
            font-family: 'Fira Code', 'Cascadia Code', monospace;
            font-size: 0.9rem;
            color: #e2e8f0;
            white-space: pre-wrap;
            border-left: 4px solid #3b82f6;
        }
        .status-active { color: #10b981; }
        .status-inactive { color: #ef4444; }
    </style>
</head>
<body>
    <div class="container">
EOM

source "$DIR/$PROJECTE/$DIR_CONF/$CONF_IFWAN"
current_mode=$(echo "$IFW_MODE" | tr '[:lower:]' '[:upper:]')
badge_class="badge-dhcp"
[[ "$IFW_MODE" == "manual" ]] && badge_class="badge-manual"

comand=$(echo "$QUERY_STRING" | sed -n 's/^.*comand=\([^&]*\).*$/\1/p')

# Icono según comando
icon="⚡"
case "$comand" in
    iniciar) icon="🚀" ;;
    aturar)  icon="🛑" ;;
    estat)   icon="📊" ;;
esac

echo '<div class="card">'
echo "  <div class='card-header'>"
echo "      <h3 class='card-title'>$icon Acció: $comand</h3>"
echo "      <span class='badge $badge_class'>$current_mode</span>"
echo "  </div>"
echo "  <div class='output-box'>"
echo "$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli ifwan $comand)"
echo "  </div>"
echo '</div>'

# Si el comando no es "estat", mostramos también el estado actual
if [[ "$comand" != "estat" ]]; then
    echo '<div class="card">'
    echo "  <div class='card-header'>"
    echo "      <h3 class='card-title'>🔍 Estat actual</h3>"
    echo "      <span class='badge $badge_class'>$current_mode</span>"
    echo "  </div>"
    echo "  <div class='output-box'>"
    echo "$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli ifwan estat)"
    echo "  </div>"
    echo '</div>'
fi

echo '    </div>'
echo '</body>'
echo '</html>'