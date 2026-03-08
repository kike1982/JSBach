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
</head>
<body>
<div class="menu-container">
    <a href="/cgi-bin/portal-captiu.cgi?comand=iniciar" target="body" class="menu-item"><span class="label">Portal Iniciar</span></a>
    <a href="/cgi-bin/portal-captiu.cgi?comand=aturar" target="body" class="menu-item"><span class="label">Portal Aturar</span></a>
    <a href="/cgi-bin/portal-captiu.cgi?comand=estat" target="body" class="menu-item"><span class="label">Portal Estat</span></a>
    <a href="/cgi-bin/portal-captiu-configurar.cgi" target="body" class="menu-item"><span class="label">Configuracio</span></a>
</div>
</body>
</html>
EOM
