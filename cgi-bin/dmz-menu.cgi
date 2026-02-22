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
    <a href="/cgi-bin/dmz.cgi?comand=iniciar" target="body" class="menu-item"><span class="icon">🚀</span><span class="label">DMZ Iniciar</span></a>
    <a href="/cgi-bin/dmz.cgi?comand=aturar" target="body" class="menu-item"><span class="icon">🛑</span><span class="label">DMZ Aturar</span></a>
    <a href="/cgi-bin/dmz.cgi?comand=estat" target="body" class="menu-item"><span class="icon">📊</span><span class="label">DMZ Estat</span></a>
    <a href="/cgi-bin/dmz-configurar.cgi" target="body" class="menu-item"><span class="icon">🛠️</span><span class="label">DMZ Configuració</span></a>
</div>
</body>
</html>
EOM
