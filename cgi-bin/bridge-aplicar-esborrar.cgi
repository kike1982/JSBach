#!/bin/bash

source /usr/local/JSBach/conf/variables.conf
RUTA="$DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli"

urldecode() {
    local data="${1//+/ }"      # Canvia + per espai
    printf '%b' "${data//%/\\x}" # Converteix %xx en caràcters
}

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="utf-8">
    <title>Resultat Operació</title>
    <style>
        /* --- Estil Modern Dark --- */
        body {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background: #0f172a;
            color: #f8fafc;
            margin: 0;
            padding: 24px;
            line-height: 1.6;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }
        .container {
            max-width: 700px;
            width: 100%;
        }
        h2 {
            text-align: center;
            color: #f8fafc;
            margin-bottom: 30px;
            font-weight: 800;
        }
        .card {
            background: #1e293b;
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 32px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
            text-align: center;
        }
        .output-box {
            background: #0f172a;
            border-radius: 8px;
            padding: 20px;
            font-family: 'Fira Code', monospace;
            font-size: 0.9rem;
            color: #e2e8f0;
            white-space: pre-wrap;
            border-left: 4px solid #ef4444;
            text-align: left;
            margin-top: 20px;
        }
        .redirect-text {
            margin-top: 20px;
            color: #94a3b8;
            font-size: 0.9rem;
        }
        .icon {
            font-size: 4rem;
            margin-bottom: 20px;
            display: block;
        }
        .success { border-left-color: #10b981; }
        .error { border-left-color: #ef4444; }
    </style>
    <script>
        setTimeout(() => {
            window.location.href = '/cgi-bin/bridge-configurar.cgi';
        }, 3000);
    </script>
</head>
<body>
    <div class="container">
EOM

# Extreiem els valors del QUERY_STRING
vid=$(echo "$QUERY_STRING" | sed -n 's/^.*vid=\([^&]*\).*$/\1/p')

# Ejecutar el comando de borrado y capturar la salida
RESULTADO="$($RUTA bridge configurar esborrar vlan "$vid")"

if echo "$RESULTADO" | grep -qi "Error"; then
    echo "        <div class='card'>"
    echo "            <span class='icon'>❌</span>"
    echo "            <h2>Error en l'eliminació</h2>"
    echo "            <div class='output-box error'>$RESULTADO</div>"
else
    echo "        <div class='card'>"
    echo "            <span class='icon'>🗑️</span>"
    echo "            <h2>VLAN eliminada correctament</h2>"
    echo "            <div class='output-box success'>VLAN amb VID $vid s'ha suprimit del sistema correctament.</div>"
fi

cat << 'EOM'
            <div class="redirect-text">
                Redirigint a la gestió de VLANs en 3 segons...
            </div>
        </div>
    </div>
</body>
</html>
EOM
