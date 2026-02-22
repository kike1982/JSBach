#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

/bin/cat << EOM
<!DOCTYPE html>
<html lang="es">
<head>
    <link rel="stylesheet" href="/cgi-bin/style.cgi">
    <meta charset="utf-8">
    <title>Gestió Bridge</title>
</head>
<body>
    <div class="container">
EOM

comand=$(echo "$QUERY_STRING" | sed -n 's/^.*comand=\([^&]*\).*$/\1/p')

# Obtener estado para el badge
status_raw=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge estat)
badge_text="DESACTIVAT"
badge_class="badge-inactive"
if echo "$status_raw" | grep -qw "^ACTIVAT"; then
    badge_text="ACTIVAT"
    badge_class="badge-active"
fi

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
echo "      <span class='badge $badge_class'>$badge_text</span>"
echo "  </div>"
echo "  <div class='output-box'>"
echo "$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge $comand)"
echo "  </div>"
echo '</div>'

# Si el comando no es "estat", mostramos también el estado actual
if [[ "$comand" != "estat" ]]; then
    echo '<div class="card">'
    echo "  <div class='card-header'>"
    echo "      <h3 class='card-title'>🔍 Estat actual</h3>"
    echo "      <span class='badge $badge_class'>$badge_text</span>"
    echo "  </div>"
    echo "  <div class='output-box'>"
    echo "$status_raw"
    echo "  </div>"
    echo '</div>'
fi

echo '    </div>'
echo '</body>'
echo '</html>'