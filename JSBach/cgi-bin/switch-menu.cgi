#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
    <link rel="stylesheet" href="/cgi-bin/style.cgi">
<meta charset="utf-8">
</head>
<body>
  <h2>Mòdul Switch</h2>
  <a href="/cgi-bin/switch.cgi?comand=estat" target="body"><span class="icon"></span> Estat Switch</a>
  <a href="/cgi-bin/switch.cgi?comand=mostrar" target="body"><span class="icon"></span> Taula MAC</a>
  <a href="/cgi-bin/switch.cgi?comand=gestion_mac" target="body"><span class="icon"></span> Gestión de MAC</a>
  <a href="/cgi-bin/switch.cgi?comand=gestion_admin" target="body"><span class="icon"></span> Gestión de Admin</a>
  <a href="/cgi-bin/switch.cgi?comand=configurar" target="body"><span class="icon"></span> Configuració</a>
</body>
</html>
EOF
