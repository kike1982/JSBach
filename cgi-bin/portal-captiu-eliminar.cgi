#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

USUARI=$(echo "$QUERY_STRING" | sed -n 's/^.*usuari=\([^&]*\).*$/\1/p')

RESULTAT=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli portal-captiu configurar eliminar_usuari "$USUARI")

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
    <title>Eliminar usuari - Portal Captiu</title>
    <meta http-equiv="refresh" content="2;url=/cgi-bin/portal-captiu-configurar.cgi">
</head>
<body>
<div class="container">
    <div class="card card-portal">
        <h2>Eliminar usuari del portal captiu</h2>
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
