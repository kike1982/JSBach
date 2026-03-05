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
            window.location.href = '/cgi-bin/bridge-configurar-taguntag.cgi';
        }, 3000);
    </script>
</head>
<body>
    <div class="container">
        <div class="card">
            <span class="success-icon"></span>
            <h2>Tag-Untag Modificat</h2>
EOM

int=$(echo "$QUERY_STRING" | sed -n 's/^.*int=\([^&]*\).*$/\1/p')
tag=$(echo "$QUERY_STRING" | sed -n 's/^.*tag=\([^&]*\).*$/\1/p')
untag=$(echo "$QUERY_STRING" | sed -n 's/^.*untag=\([^&]*\).*$/\1/p')

tag=$(urldecode "$tag")

cat << EOM
            <div class="info-grid">
                <div class="info-item"><span class="info-label">Interfaç</span><span class="info-value">$int</span></div>
                <div class="info-item"><span class="info-label">Untag</span><span class="info-value">$untag</span></div>
                <div class="info-item"><span class="info-label">Tag</span><span class="info-value">$tag</span></div>
            </div>

            <div class="output-box">
$($RUTA bridge configurar guardar bridge "$int" "$untag" "$tag")
            </div>

            <div class="redirect-text">
                Redirigint a la configuració Tag-Untag en 3 segons...
            </div>
        </div>
    </div>
</body>
</html>
EOM
