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
<h4><a href="/cgi-bin/ifwan.cgi?comand=iniciar&" target="body">Iniciar WAN</a></h4>
<h4><a href="/cgi-bin/ifwan.cgi?comand=aturar&" target="body">Aturar WAN</a></h4>
<h4><a href="/cgi-bin/ifwan.cgi?comand=estat&" target="body">Estat Actual</a></h4>
<h4><a href="/cgi-bin/ifwan-configurar.cgi" target="body">Configuració</a></h4>
</body>
</html>

EOM