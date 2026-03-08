#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

ACCIO=$(echo "$QUERY_STRING" | sed -n 's/^.*accio=\([^&]*\).*$/\1/p')

case "$ACCIO" in
    activar)
        RESULTAT=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli portal-captiu configurar activar_cron)
        TITLE="Activar cron"
        ;;
    desactivar)
        RESULTAT=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli portal-captiu configurar desactivar_cron)
        TITLE="Desactivar cron"
        ;;
    netejar)
        RESULTAT=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli portal-captiu configurar netejar_sessions)
        TITLE="Netejar sessions"
        ;;
    *)
        RESULTAT="ERROR: Accio no reconeguda: $ACCIO"
        TITLE="Error"
        ;;
esac

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
    <title>$TITLE - Portal Captiu</title>
    <meta http-equiv="refresh" content="2;url=/cgi-bin/portal-captiu-configurar.cgi">
</head>
<body>
<div class="container">
    <div class="card card-portal">
        <h2>$TITLE</h2>
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
