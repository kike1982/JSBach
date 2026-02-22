#!/bin/bash

source /usr/local/JSBach/conf/variables.conf


echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="UTF-8">
<title>Gestió VLANs</title>
<style>
/* --- Estil Modern Dark --- */
body {
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #0f172a;
    color: #f8fafc;
    margin: 0;
    padding: 24px;
    line-height: 1.6;
}
.container {
    max-width: 900px;
    margin: 0 auto;
}
h2 {
    color: #3b82f6;
    margin-top: 40px;
    margin-bottom: 20px;
    font-size: 1.5rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border-left: 4px solid #3b82f6;
    padding-left: 15px;
}
.card {
    background: #1e293b;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
}
table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
}
th {
    text-align: left;
    color: #64748b;
    padding: 12px 8px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    font-size: 0.85rem;
    text-transform: uppercase;
}
td {
    padding: 15px 8px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    color: #f1f5f9;
}
.btn {
    padding: 8px 14px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
    font-size: 0.85rem;
    transition: all 0.2s;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    margin-right: 8px;
}
.btn-edit { background: #3b82f6; color: white; }
.btn-edit:hover { background: #2563eb; transform: translateY(-1px); }
.btn-delete { background: #ef4444; color: white; }
.btn-delete:hover { background: #dc2626; transform: translateY(-1px); }
.btn-create { 
    background: #10b981; 
    color: white; 
    padding: 12px 24px; 
    font-size: 1rem; 
    margin-top: 20px;
    display: block;
    width: fit-content;
    margin-left: auto;
}
.btn-create:hover { background: #059669; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3); }

.vlan-name { font-weight: 700; color: #3b82f6; }
.vlan-vid { font-family: monospace; background: rgba(255,255,255,0.05); padding: 2px 6px; border-radius: 4px; }
</style>
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
