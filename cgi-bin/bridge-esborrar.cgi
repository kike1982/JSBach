#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

QUERY_STRING=${QUERY_STRING:-$1}
VID=$(echo "$QUERY_STRING" | sed -n 's/.*vid=\([0-9]*\).*/\1/p')

echo "<html><head>
    <link rel="stylesheet" href="/cgi-bin/style.cgi"><title>Esborrar VLAN</title>"
echo "<meta charset='utf-8'>"

cat << 'EOF'
<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="UTF-8">
<title>Esborrar VLAN</title>
</head>
<body>
<div class="container">
EOM

VLAN_DATA="$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge configurar mostrar vlan)"
mapfile -t VLANS <<< "$VLAN_DATA"

FOUND_LINE=""
for line in "${VLANS[@]}"; do
    IFS=';' read -r nom vid subnet gw _ <<< "$line"
    if [ "$vid" == "$VID" ]; then
        FOUND_LINE="$line"
        break
    fi
done

if [ -z "$FOUND_LINE" ]; then
    echo "<h2>Error</h2>"
    echo "<div class='card'>No s'ha trobat cap VLAN amb VID = $VID</div>"
    echo "<a href='/cgi-bin/bridge-configurar.cgi' class='btn btn-back'>⬅Tornar</a>"
    echo "</div></body></html>"
    exit 0
fi

IFS=';' read -r nom vid subnet gw _ <<< "$FOUND_LINE"

echo "    <h2>Confirmar Eliminació</h2>"
echo "    <div class='card'>"
echo "        <div class='warning-box'>Estàs segur que vols eliminar aquesta VLAN? Aquesta acció no es pot desfer.</div>"
echo "        <div class='info-grid'>"
echo "            <div class='info-item'><span class='info-label'>Nom</span><span class='info-value'>$nom</span></div>"
echo "            <div class='info-item'><span class='info-label'>VID</span><span class='info-value'>$vid</span></div>"
echo "            <div class='info-item'><span class='info-label'>Subxarxa</span><span class='info-value'>$subnet</span></div>"
echo "            <div class='info-item'><span class='info-label'>Gateway</span><span class='info-value'>$gw</span></div>"
echo "        </div>"
echo "        <form action='/cgi-bin/bridge-aplicar-esborrar.cgi' method='get'>"
echo "            <input type='hidden' name='vid' value='$vid'>"
echo "            <div class='btn-group'>"
echo "                <a href='/cgi-bin/bridge-configurar.cgi' class='btn btn-back'>⬅Cancel·lar</a>"
echo "                <button type='submit' class='btn btn-delete'>Esborrar VLAN</button>"
echo "            </div>"
echo "        </form>"
echo "    </div>"
echo "</div>"
echo "</body></html>"
