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
    <link rel="stylesheet" href="/cgi-bin/style.cgi">
    <meta charset="utf-8">
    <title>Resultat Operació</title>
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
    echo "            <span class='icon'></span>"
    echo "            <h2>Error en l'eliminació</h2>"
    echo "            <div class='output-box error'>$RESULTADO</div>"
else
    echo "        <div class='card'>"
    echo "            <span class='icon'></span>"
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
