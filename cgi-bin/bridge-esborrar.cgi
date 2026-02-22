#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

QUERY_STRING=${QUERY_STRING:-$1}
VID=$(echo "$QUERY_STRING" | sed -n 's/.*vid=\([0-9]*\).*/\1/p')

echo "<html><head><title>Esborrar VLAN</title>"
echo "<meta charset='utf-8'>"

cat << 'EOF'
<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="UTF-8">
<title>Esborrar VLAN</title>
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
    max-width: 800px;
    margin: 0 auto;
}
h2 {
    text-align: center;
    color: #ef4444;
    margin-bottom: 30px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.card {
    background: #1e293b;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 32px;
    margin-bottom: 24px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    text-align: center;
}
.warning-box {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid #ef4444;
    color: #f87171;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 24px;
    font-weight: 600;
}
.info-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
    text-align: left;
    margin-bottom: 30px;
}
.info-item {
    background: rgba(255,255,255,0.05);
    padding: 12px;
    border-radius: 8px;
}
.info-label { color: #64748b; font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 4px; }
.info-value { color: #f1f5f9; font-weight: 700; font-family: monospace; }

.btn-group {
    display: flex;
    gap: 15px;
}
.btn {
    flex: 1;
    padding: 14px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 700;
    font-size: 1rem;
    transition: all 0.2s;
    text-transform: uppercase;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
    text-decoration: none;
}
.btn-delete { background: #ef4444; color: white; }
.btn-delete:hover { background: #dc2626; transform: translateY(-1px); box-shadow: 0 10px 15px -3px rgba(239, 68, 68, 0.3); }
.btn-back { background: #475569; color: white; }
.btn-back:hover { background: #334155; transform: translateY(-1px); }
</style>
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
    echo "<h2>❌ Error</h2>"
    echo "<div class='card'>No s'ha trobat cap VLAN amb VID = $VID</div>"
    echo "<a href='/cgi-bin/bridge-configurar.cgi' class='btn btn-back'>⬅️ Tornar</a>"
    echo "</div></body></html>"
    exit 0
fi

IFS=';' read -r nom vid subnet gw _ <<< "$FOUND_LINE"

echo "    <h2>⚠️ Confirmar Eliminació</h2>"
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
echo "                <a href='/cgi-bin/bridge-configurar.cgi' class='btn btn-back'>⬅️ Cancel·lar</a>"
echo "                <button type='submit' class='btn btn-delete'>🗑️ Esborrar VLAN</button>"
echo "            </div>"
echo "        </form>"
echo "    </div>"
echo "</div>"
echo "</body></html>"
