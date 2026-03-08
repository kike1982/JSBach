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
    <title>Portal Captiu</title>
</head>
<body>
<div class="container">
EOM

comand=$(echo "$QUERY_STRING" | sed -n 's/^.*comand=\([^&]*\).*$/\1/p')

echo "<div class='card card-portal'>"
echo "  <h2>Comanda: $comand</h2>"
echo "  <div class='output'>"
echo "    <pre>$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli portal-captiu "$comand")</pre>"
echo "  </div>"

if [[ "$comand" != "estat" ]]; then
    estat_actual=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli portal-captiu estat)
    if [[ "$estat_actual" == "$ACTIVAT" ]]; then
        badge_class="badge badge-ok"
    else
        badge_class="badge badge-err"
    fi
    echo "  <div class='mt-md'><span class='$badge_class'>$estat_actual</span> Estat actual del portal captiu</div>"
fi
echo "</div>"

cat << EOM
</div>
</body>
</html>
EOM
