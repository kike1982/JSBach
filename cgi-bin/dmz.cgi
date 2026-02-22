#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
    <link rel="stylesheet" href="/cgi-bin/style.cgi">
    <meta charset="utf-8">
    <title>Estat DMZ</title>
</head>
<body>
<div class="container">
EOM

comand=$(echo "$QUERY_STRING" | sed -n 's/^.*comand=\([^&]*\).*$/\1/p')

# Emojis según comanda
case "$comand" in
    iniciar) ICON="🚀";;
    aturar)  ICON="🛑";;
    estat)   ICON="📊";;
    *)       ICON="⚙️";;
esac

echo "<div class='card'>"
echo "  <h2>$ICON Comanda: $comand</h2>" 
echo "  <div class='output'>"
echo "    <pre>$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dmz "$comand")</pre>"
echo "  </div>"

# Si no es 'estat', mostrar también el estado actual
if [[ "$comand" != "estat" ]]; then
    estat_actual=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dmz estat)
    echo "  <div class='status-badge'><span>🔍</span> Estat actual DMZ: $estat_actual</div>"
fi
echo "</div>"

cat << EOM
</div>
</body>
</html>
EOM
