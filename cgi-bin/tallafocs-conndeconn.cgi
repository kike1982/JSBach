#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

urldecode() {
    local data="${1//+/ }"
    printf '%b' "${data//%/\\x}"
}

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
    <link rel="stylesheet" href="/cgi-bin/style.cgi">
    <meta charset="utf-8">
    <title>Resultat Operació</title>
    <script>
        setTimeout(() => {
            window.location.href = '/cgi-bin/tallafocs-configuracio.cgi';
        }, 3000);
    </script>
</head>
<body>
    <div class="container">
EOM

accio=$(echo "$QUERY_STRING" | sed -n 's/^.*accio=\([^&]*\).*$/\1/p')
id=$(echo "$QUERY_STRING" | sed -n 's/^.*id=\([^&]*\).*$/\1/p')

accio=$(urldecode "$accio")
id=$(urldecode "$id")

echo "      <div class='card'>"
echo "          <span class='icon'></span>"
echo "          <h2>Operació Sol·licitada</h2>"
echo "          <div class='info-grid'>"
echo "              <div class='info-item'><span class='info-label'>Acció</span><span class='info-value'>$accio</span></div>"
echo "              <div class='info-item'><span class='info-label'>Identificador</span><span class='info-value'>$id</span></div>"
echo "          </div>"
echo "          <div class='output-box'><pre>$("$DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli" tallafocs configurar "$accio" "$id")</pre></div>"
echo "          <div class='redirect-text'>Redirigint a la configuració en 3 segons...</div>"
echo "      </div>"

cat << EOM
    </div>
</body>
</html>
EOM
