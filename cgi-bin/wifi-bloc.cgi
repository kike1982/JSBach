#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

MAC=$(echo "$QUERY_STRING" | sed -n 's/^.*mac=\([^&]*\).*$/\1/p')
ACCIO=$(echo "$QUERY_STRING" | sed -n 's/^.*accio=\([^&]*\).*$/\1/p')

RESULTAT=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli wifi configurar "$ACCIO" "$MAC")

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
    <link rel="stylesheet" href="/cgi-bin/style.cgi">
    <meta charset="utf-8">
    <title>Bloqueig WiFi</title>
</head>
<body>
<div class="container">
    <div class="card">
        <h2>🔒 Control d'accés MAC</h2>
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
