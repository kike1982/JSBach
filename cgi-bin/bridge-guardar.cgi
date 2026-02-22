#!/bin/bash

source /usr/local/JSBach/conf/variables.conf
RUTA="$DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli"

urldecode() {
    local data="${1//+/ }"
    printf '%b' "${data//%/\\x}"
}

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
    <link rel="stylesheet" href="/cgi-bin/style.cgi">
    <meta charset="utf-8">
    <title>Resultat Operació</title>
    <script>
        setTimeout(() => {
            window.location.href = '/cgi-bin/bridge-configurar.cgi';
        }, 3000);
    </script>
</head>
<body>
    <div class="container">
        <div class="card">
            <span class="success-icon">✅</span>
            <h2>Operació Completada</h2>
EOM

# ----------------------------------------------------
# Obtener parámetros
# ----------------------------------------------------
nom=$(echo "$QUERY_STRING" | sed -n 's/^.*nom=\([^&]*\).*$/\1/p')
vid=$(echo "$QUERY_STRING" | sed -n 's/^.*vid=\([^&]*\).*$/\1/p')
ipmasc=$(echo "$QUERY_STRING" | sed -n 's/^.*ipmasc=\([^&]*\).*$/\1/p')
ippe=$(echo "$QUERY_STRING" | sed -n 's/^.*ippe=\([^&]*\).*$/\1/p')

nom=$(urldecode "$nom")
ipmasc=$(urldecode "$ipmasc")
ippe=$(urldecode "$ippe")

cat << EOM
            <div class="info-grid">
                <div class="info-item"><span class="info-label">Nom</span><span class="info-value">$nom</span></div>
                <div class="info-item"><span class="info-label">VID</span><span class="info-value">$vid</span></div>
                <div class="info-item"><span class="info-label">Xarxa</span><span class="info-value">$ipmasc</span></div>
                <div class="info-item"><span class="info-label">Gateway</span><span class="info-value">$ippe</span></div>
            </div>

            <div class="output-box">
$($RUTA bridge configurar guardar vlan "$nom" "$vid" "$ipmasc" "$ippe")
            </div>

            <div class="redirect-text">
                Redirigint a la gestió de VLANs en 3 segons...
            </div>
        </div>
    </div>
</body>
</html>
EOM
