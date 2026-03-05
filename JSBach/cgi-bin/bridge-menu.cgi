#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

/bin/cat << EOM

<!DOCTYPE html>
<html lang="es">
<head>
    <link rel="stylesheet" href="/cgi-bin/style.cgi">
    <meta charset="utf-8">
</head>
<body>
    <h4><a href="/cgi-bin/bridge.cgi?comand=iniciar&" target="body">Iniciar Bridge</a></h4>
    <h4><a href="/cgi-bin/bridge.cgi?comand=aturar&" target="body">Aturar Bridge</a></h4>
    <h4><a href="/cgi-bin/bridge.cgi?comand=estat&" target="body">Estat Actual</a></h4>
    <h4><a href="/cgi-bin/bridge-configurar-taguntag.cgi" target="body">Tag / Untag</a></h4>
    <h4><a href="/cgi-bin/bridge-configurar-ebtables.cgi" target="body">Aïllament (ebtables)</a></h4>
    <h4><a href="/cgi-bin/bridge-configurar.cgi" target="body">Gestió VLANs</a></h4>
</body>
</html>
EOM