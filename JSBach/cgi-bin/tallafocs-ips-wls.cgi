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
    <title>Resultat Operació IP WLS</title>
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
vid=$(echo "$QUERY_STRING" | sed -n 's/^.*vid=\([^&]*\).*$/\1/p')
ip=$(echo "$QUERY_STRING" | sed -n 's/^.*ip=\([^&]*\).*$/\1/p')
mac=$(echo "$QUERY_STRING" | sed -n 's/^.*mac=\([^&]*\).*$/\1/p')

accio=$(urldecode "$accio")
vid=$(urldecode "$vid")
ip=$(urldecode "$ip")
mac=$(urldecode "$mac")

echo "      <div class='card'>"
echo "          <span class='icon'></span>"
echo "          <h2>Whitelist d'IPs</h2>"
echo "          <div class='info-grid'>"
echo "              <div class='info-item'><span class='info-label'>Acció</span><span class='info-value'>$accio</span></div>"
echo "              <div class='info-item'><span class='info-label'>VID</span><span class='info-value'>$vid</span></div>"
echo "              <div class='info-item'><span class='info-label'>IP</span><span class='info-value'>$ip</span></div>"
echo "              <div class='info-item'><span class='info-label'>MAC</span><span class='info-value'>$mac</span></div>"
echo "          </div>"
echo "          <div class='output-box'><pre>$("$DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli" tallafocs configurar "$accio" "$vid" "$ip" "$mac")</pre></div>"
echo "          <div class='redirect-text'>Redirigint a la configuració en 3 segons...</div>"
echo "      </div>"

cat << EOM
    </div>
</body>
</html>
EOM
