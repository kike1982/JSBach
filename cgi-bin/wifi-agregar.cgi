#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

MAC=$(echo "$QUERY_STRING" | sed -n 's/^.*mac=\([^&]*\).*$/\1/p')
IP=$(echo "$QUERY_STRING" | sed -n 's/^.*ip=\([^&]*\).*$/\1/p')
NOM=$(echo "$QUERY_STRING" | sed -n 's/^.*nom=\([^&]*\).*$/\1/p')

# URL decode bàsic (+ -> espai)
NOM=$(echo "$NOM" | sed 's/+/ /g')

RESULTAT=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli wifi configurar afegir "$MAC" "$IP" "$NOM")

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
    <link rel="stylesheet" href="/cgi-bin/style.cgi">
    <meta charset="utf-8">
    <title>Afegint client WiFi</title>
</head>
<body>
<div class="container">
    <div class="card">
        <h2>🖥️ Afegir client WiFi</h2>
        <div class="output"><pre>$RESULTAT</pre></div>
        <script>
            setTimeout(() => {
                window.location.href = '/cgi-bin/wifi-configurar.cgi';
            }, 2000);
        </script>
        <p>Tornant a la configuració...</p>
    </div>
</div>
</body>
</html>
EOM
