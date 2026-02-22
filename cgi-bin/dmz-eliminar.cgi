#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

# --- Cabecera HTML ---
cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
    <link rel="stylesheet" href="/cgi-bin/style.cgi">
    <meta charset="utf-8">
    <title>Resultat Operació DMZ</title>
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
