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
<meta charset="UTF-8">
<title>Modificar VLAN</title>
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
    color: #3b82f6;
    margin-bottom: 30px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.card {
    background: #1e293b;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
}
.card-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 20px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    padding-bottom: 12px;
}
.card-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #94a3b8;
    margin: 0;
}
.form-group {
    margin-bottom: 20px;
}
label {
    display: block;
    margin-bottom: 8px;
    font-weight: 600;
    color: #cbd5e1;
    font-size: 0.9rem;
}
input[type="text"] {
    width: 100%;
    padding: 12px;
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 8px;
    color: #f8fafc;
    font-family: 'Fira Code', monospace;
    transition: all 0.2s;
    box-sizing: border-box;
}
input[type="text"]:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}
input[readonly] {
    background: #1e293b;
    color: #64748b;
    cursor: not-allowed;
    border-style: dashed;
}
.btn-group {
    display: flex;
    gap: 15px;
    margin-top: 32px;
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
    letter-spacing: 0.025em;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
    text-decoration: none;
}
.btn-submit { background: #3b82f6; color: white; }
.btn-submit:hover { background: #2563eb; transform: translateY(-1px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3); }
.btn-back { background: #475569; color: white; }
.btn-back:hover { background: #334155; transform: translateY(-1px); }

#errorBox {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid #ef4444;
    color: #f87171;
    padding: 16px;
    border-radius: 8px;
    margin-bottom: 24px;
    display: none;
    font-size: 0.9rem;
}
</style>
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
