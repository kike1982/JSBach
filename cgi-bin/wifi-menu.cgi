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
    <a href="/cgi-bin/wifi.cgi?comand=iniciar" target="body" class="menu-item"><span class="icon"></span><span class="label">WiFi Iniciar</span></a>
    <a href="/cgi-bin/wifi.cgi?comand=aturar" target="body" class="menu-item"><span class="icon"></span><span class="label">WiFi Aturar</span></a>
    <a href="/cgi-bin/wifi.cgi?comand=estat" target="body" class="menu-item"><span class="icon"></span><span class="label">WiFi Estat</span></a>
    <a href="/cgi-bin/wifi-configurar.cgi" target="body" class="menu-item"><span class="icon"></span><span class="label">WiFi Configuració</span></a>
</div>
</body>
</html>
EOM
