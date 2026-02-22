#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

/bin/cat <<'EOM'
<!DOCTYPE html>
<html lang="es">
<head>
    <link rel="stylesheet" href="/cgi-bin/style.cgi">
    <meta charset="utf-8">
    <title>Gestió WAN</title>
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