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
    <title>Estat WiFi AP</title>
</head>
<body>
<div class="container">
EOM

comand=$(echo "$QUERY_STRING" | sed -n 's/^.*comand=\([^&]*\).*$/\1/p')

case "$comand" in
    iniciar) ICON="";;
    aturar)  ICON="";;
    estat)   ICON="📡";;
    *)       ICON="";;
esac

echo "<div class='card'>"
echo "  <h2>$ICON Comanda: $comand</h2>"
echo "  <div class='output'>"
echo "    <pre>$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli wifi "$comand")</pre>"
echo "  </div>"

if [[ "$comand" != "estat" ]]; then
    estat_actual=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli wifi estat)
    echo "  <div class='status-badge'><span></span> Estat actual WiFi AP: $estat_actual</div>"
fi
echo "</div>"

cat << EOM
</div>
</body>
</html>
EOM
