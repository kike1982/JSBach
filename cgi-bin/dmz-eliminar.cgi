#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

# --- Cabecera HTML ---
cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="utf-8">
    <title>Resultat Operació DMZ</title>
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
            font-size: 0.85rem;
        }
        .icon {
            font-size: 4rem;
            margin-bottom: 20px;
            display: block;
        }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-top: 20px;
            text-align: left;
            font-size: 0.9rem;
        }
        .info-item {
            background: rgba(255,255,255,0.05);
            padding: 10px;
            border-radius: 6px;
        }
        .info-label { color: #64748b; font-weight: 600; display: block; margin-bottom: 4px; }
        .info-value { color: #ef4444; font-weight: 700; }
    </style>
    <script>
        setTimeout(() => {
            window.location.href = '/cgi-bin/dmz-configurar.cgi';
        }, 3000);
    </script>
</head>
<body>
    <div class="container">
EOM

# --- Función para decodificar URL ---
urldecode() {
    echo -e "$(sed 's/+/ /g;s/%/\\x/g' <<< "$1")"
}

# --- Función para obtener parámetros ---
get_param() {
    local name=$1
    local value=$(echo "$QUERY_STRING" | tr '&' '\n' | grep "^$name=" | cut -d'=' -f2-)
    urldecode "$value"
}

# --- Obtener parámetros correctamente ---
PORT=$(get_param "port" | xargs)
PROTO=$(get_param "proto" | xargs)
IP_DMZ=$(get_param "ipdmz" | xargs)

echo "      <div class='card'>"
echo "          <span class='icon'>🗑️</span>"
echo "          <h2>Servei DMZ Eliminat</h2>"
echo "          <div class='info-grid'>"
echo "              <div class='info-item'><span class='info-label'>Port</span><span class='info-value'>$PORT</span></div>"
echo "              <div class='info-item'><span class='info-label'>Protocol</span><span class='info-value'>$PROTO</span></div>"
echo "              <div class='info-item'><span class='info-label'>IP Servidor</span><span class='info-value'>$IP_DMZ</span></div>"
echo "          </div>"
echo "          <div class='output-box'>"
$DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli dmz configurar eliminar "$PORT" "$PROTO" "$IP_DMZ"
echo "          </div>"
echo "          <div class='redirect-text'>Redirigint a la configuració en 3 segons...</div>"
echo "      </div>"

cat << EOM
    </div>
</body>
</html>
EOM
