#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

USUARI=$(echo "$QUERY_STRING" | sed -n 's/^.*usuari=\([^&]*\).*$/\1/p')
PASS=$(echo "$QUERY_STRING" | sed -n 's/^.*pass=\([^&]*\).*$/\1/p')

# URL decode simple
USUARI=$(echo "$USUARI" | sed 's/+/ /g; s/%20/ /g')
PASS=$(echo "$PASS" | sed 's/+/ /g; s/%20/ /g')

RESULTAT=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli portal-captiu configurar afegir_usuari "$USUARI" "$PASS")

if echo "$RESULTAT" | grep -q "^OK"; then
    MSG_CLASS="alert alert-ok"
    MSG_ICON=""
else
    MSG_CLASS="alert alert-err"
    MSG_ICON=""
fi

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
    <link rel="stylesheet" href="/cgi-bin/style.cgi">
    <meta charset="utf-8">
    <title>Afegir usuari - Portal Captiu</title>
    <meta http-equiv="refresh" content="2;url=/cgi-bin/portal-captiu-configurar.cgi">
</head>
<body>
<div class="container">
    <div class="card card-portal">
        <h2>Afegir usuari al portal captiu</h2>
        <div class="$MSG_CLASS">$MSG_ICON $RESULTAT</div>
        <p class="redirect-text">Redirigint a la configuracio...</p>
        <div class="btn-group mt-md">
            <a href="/cgi-bin/portal-captiu-configurar.cgi" class="btn btn-ghost">Tornar</a>
        </div>
    </div>
</div>
</body>
</html>
EOM
