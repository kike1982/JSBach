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
    <title>Resultat Operació DMZ</title>
    <script>
        setTimeout(() => {
            window.location.href = '/cgi-bin/dmz-configurar.cgi';
        }, 3000);
    </script>
</head>
<body>
    <div class="container">
EOM

PORT=$(echo "$QUERY_STRING" | sed -n 's/^.*port=\([^&]*\).*$/\1/p')
PROTO=$(echo "$QUERY_STRING" | sed -n 's/^.*proto=\([^&]*\).*$/\1/p')
IP_DMZ=$(echo "$QUERY_STRING" | sed -n 's/^.*ipdmz=\([^&]*\).*$/\1/p')

echo "      <div class='card'>"
echo "          <span class='icon'>➕</span>"
echo "          <h2>Servei DMZ Afegit</h2>"
echo "          <div class='info-grid'>"
echo "              <div class='info-item'><span class='info-label'>Port</span><span class='info-value'>$PORT</span></div>"
echo "              <div class='info-item'><span class='info-label'>Protocol</span><span class='info-value'>$PROTO</span></div>"
echo "              <div class='info-item'><span class='info-label'>IP Servidor</span><span class='info-value'>$IP_DMZ</span></div>"
echo "          </div>"
echo "          <div class='output-box'>"
$DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli dmz configurar afegir "$PORT" "$PROTO" "$IP_DMZ"
echo "          </div>"
echo "          <div class='redirect-text'>Redirigint a la configuració en 3 segons...</div>"
echo "      </div>"

cat << EOM
    </div>
</body>
</html>
EOM

