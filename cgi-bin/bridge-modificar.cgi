#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

QUERY_STRING=${QUERY_STRING:-$1}  
VID=$(echo "$QUERY_STRING" | sed -n 's/.*vid=\([0-9]*\).*/\1/p')

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
    <link rel="stylesheet" href="/cgi-bin/style.cgi">
<meta charset="UTF-8">
<title>Modificar VLAN</title>
</head>
<body>
<div class="container">
EOM

# === Validación en JS ===
cat <<'EOF'
<script>
function validaIP(ip) {
    const regex = /^([0-9]{1,3}\.){3}[0-9]{1,3}(\/[0-9]{1,2})?$/;
    if (!regex.test(ip)) return false;
    const partes = ip.split('/');
    const octets = partes[0].split('.');
    for (let o of octets) {
        if (parseInt(o) < 0 || parseInt(o) > 255) return false;
    }
    if (partes[1] && (parseInt(partes[1]) < 1 || parseInt(partes[1]) > 32)) return false;
    return true;
}

function validarFormulario() {
    const form = document.forms['vlanForm'];
    const nom = form['nom'].value.trim();
    const ipmasc = form['ipmasc'].value.trim();
    const ippe = form['ippe'].value.trim();
    const errorBox = document.getElementById('errorBox');

    errorBox.style.display = 'none';
    errorBox.innerHTML = '';

    if (!nom || !ipmasc || !ippe) {
        errorBox.innerHTML += '⚠️ Tots els camps són obligatoris.<br>';
        errorBox.style.display = 'block';
        return false;
    }

    if (!/^[a-zA-Z0-9_-]+$/.test(nom)) {
        errorBox.innerHTML += '⚠️ El nom de VLAN només pot contenir lletres, números i guions baixos.<br>';
        errorBox.style.display = 'block';
        return false;
    }

    if (!validaIP(ipmasc)) {
        errorBox.innerHTML += '⚠️ Format d\'IP/Subxarxa incorrecte.<br>';
        errorBox.style.display = 'block';
        return false;
    }

    if (!validaIP(ippe)) {
        errorBox.innerHTML += '⚠️ IP/PE incorrecta.<br>';
        errorBox.style.display = 'block';
        return false;
    }

    return true;
}
</script>
EOF

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
    echo "<div class='card' style='text-align:center;'>No s'ha trobat cap VLAN amb VID = $VID</div>"
    echo "<div class='btn-group'><a href='/cgi-bin/bridge-configurar.cgi' class='btn btn-back'>⬅️ Tornar</a></div>"
    echo "</div></body></html>"
    exit 0
fi

IFS=';' read -r nom vid subnet gw _ <<< "$FOUND_LINE"

echo "    <h2>✏️ Modificar VLAN</h2>"
echo "    <div id='errorBox'></div>"
echo "    <form name='vlanForm' action='/cgi-bin/bridge-guardar.cgi' method='get' onsubmit='return validarFormulario()'>"
echo "        <div class='card'>"
echo "            <div class='card-header'><h3 class='card-title'>📝 Dades d'Identificació</h3></div>"
echo "            <div class='form-group'>"
echo "                <label>Nom de la VLAN:</label>"
if [ "$vid" -lt "3" ]; then
    echo "                <input type='text' name='nom' value='$nom' readonly>"
else
    echo "                <input type='text' name='nom' value='$nom'>"
fi
echo "            </div>"
echo "            <div class='form-group'>"
echo "                <label>VLAN ID (VID):</label>"
echo "                <input type='text' name='vid' value='$vid' readonly>"
echo "            </div>"
echo "        </div>"

echo "        <div class='card'>"
echo "            <div class='card-header'><h3 class='card-title'>🌐 Configuració de Xarxa</h3></div>"
echo "            <div class='form-group'>"
echo "                <label>IP / Subxarxa:</label>"
echo "                <input type='text' name='ipmasc' value='$subnet'>"
echo "            </div>"
echo "            <div class='form-group'>"
echo "                <label>Porta d'enllaç (GW):</label>"
echo "                <input type='text' name='ippe' value='$gw'>"
echo "            </div>"
echo "        </div>"

echo "        <div class='btn-group'>"
echo "            <a href='/cgi-bin/bridge-configurar.cgi' class='btn btn-back'>⬅️ Tornar</a>"
echo "            <button type='submit' class='btn btn-submit'>💾 Guardar Canvis</button>"
echo "        </div>"
echo "    </form>"
echo "</div>"
echo "</body></html>"
