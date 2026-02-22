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
<title>Gestió VLANs</title>
</head>
<body>
<div class="container">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <h1 style="color:#f8fafc; font-size:1.8rem;">🌉 Gestió de VLANs</h1>
        <a href="/cgi-bin/bridge-nova-vlan.cgi" class="btn btn-create">➕ Nova VLAN</a>
    </div>
EOM

VLAN_DATA="$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge configurar mostrar vlan)"
mapfile -t VLANS <<< "$VLAN_DATA"

if [ "${#VLANS[@]}" -lt 2 ]; then
    echo "<div class='card' style='text-align:center; color:#ef4444;'>⚠️ No hi ha prou VLANs definides al sistema.</div>"
    echo "</div></body></html>"
    exit 0
fi

# Función para renderizar una tabla de VLANs
render_vlan_table() {
    local title=$1
    local range_start=$2
    local range_end=$3
    
    echo "<h2>$title</h2>"
    echo "<div class='card'>"
    echo "<table>"
    echo "<tr><th>Nom</th><th>VID</th><th>Subxarxa</th><th>Gateway</th><th>Accions</th></tr>"
    
    for ((i=range_start; i<=range_end; i++)); do
        line="${VLANS[$i]}"
        [ -z "$line" ] && continue
        IFS=';' read -r nom vid subnet gw _ <<< "$line"
        
        echo "<tr>"
        echo "  <td><span class='vlan-name'>$nom</span></td>"
        echo "  <td><span class='vlan-vid'>$vid</span></td>"
        echo "  <td>$subnet</td>"
        echo "  <td>$gw</td>"
        echo "  <td>"
        echo "    <a href='/cgi-bin/bridge-modificar.cgi?vid=$vid' class='btn btn-edit'>✏️ Modificar</a>"
        if [ "$i" -gt 1 ]; then
            echo "    <a href='/cgi-bin/bridge-esborrar.cgi?vid=$vid' class='btn btn-delete'>🗑️ Esborrar</a>"
        fi
        echo "  </td>"
        echo "</tr>"
    done
    
    echo "</table>"
    echo "</div>"
}

# VLAN ADMINISTRACIÓ
render_vlan_table "🛡️ VLAN ADMINISTRACIÓ" 0 0

# VLAN DMZ
render_vlan_table "🔥 VLAN DMZ" 1 1

# Otras VLANs
if [ "${#VLANS[@]}" -gt 2 ]; then
    render_vlan_table "🌐 Altres VLANs" 2 $(( ${#VLANS[@]} - 1 ))
fi

echo "</div></body></html>"
