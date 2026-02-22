#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
    <link rel="stylesheet" href="/cgi-bin/style.cgi">
<meta charset="UTF-8">
</head>
<body>
    <div class="menu-title">Tallafocs (Firewall)</div>
    <div class="menu-list">
        <a href="/cgi-bin/tallafocs.cgi?comand=iniciar" class="menu-item item-start" target="body">
            <span class="icon">🚀</span> Iniciar Servei
        </a>
        <a href="/cgi-bin/tallafocs.cgi?comand=aturar" class="menu-item item-stop" target="body">
            <span class="icon">🛑</span> Aturar Servei
        </a>
        <a href="/cgi-bin/tallafocs.cgi?comand=estat" class="menu-item item-status" target="body">
            <span class="icon">📊</span> Estat Global
        </a>
        <a href="/cgi-bin/tallafocs-configuracio.cgi" class="menu-item item-config" target="body">
            <span class="icon">🛠️</span> Configuració
        </a>
        <a href="/cgi-bin/tallafocs-input.cgi" class="menu-item item-input" target="body">
            <span class="icon">📥</span> Regles d'Entrada
        </a>
    </div>
</body>
</html>
EOM

