#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

SSID=$(echo "$QUERY_STRING"      | sed -n 's/^.*ssid=\([^&]*\).*$/\1/p' | sed 's/+/ /g')
PASS=$(echo "$QUERY_STRING"      | sed -n 's/^.*pass=\([^&]*\).*$/\1/p')
CHANNEL=$(echo "$QUERY_STRING"   | sed -n 's/^.*channel=\([^&]*\).*$/\1/p')
IP=$(echo "$QUERY_STRING"        | sed -n 's/^.*ip=\([^&]*\).*$/\1/p')
PREFIX=$(echo "$QUERY_STRING"    | sed -n 's/^.*prefix=\([^&]*\).*$/\1/p')
DHCP_START=$(echo "$QUERY_STRING"| sed -n 's/^.*dhcp_start=\([^&]*\).*$/\1/p')
DHCP_END=$(echo "$QUERY_STRING"  | sed -n 's/^.*dhcp_end=\([^&]*\).*$/\1/p')

RESULTAT=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli wifi configurar guardar_xarxa \
    "$SSID" "$PASS" "$CHANNEL" "$IP" "$PREFIX" "$DHCP_START" "$DHCP_END")

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
    <link rel="stylesheet" href="/cgi-bin/style.cgi">
    <meta charset="utf-8">
    <title>Guardant configuració WiFi</title>
</head>
<body>
<div class="container">
    <div class="card">
        <h2>⚙️ Guardar configuració WiFi</h2>
        <div class="output"><pre>$RESULTAT</pre></div>
        <script>
            setTimeout(() => {
                window.location.href = '/cgi-bin/wifi-configurar.cgi';
            }, 3000);
        </script>
        <p>Tornant a la configuració...</p>
    </div>
</div>
</body>
</html>
EOM
