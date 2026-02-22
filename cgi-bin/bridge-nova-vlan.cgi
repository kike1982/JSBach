#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

# Obtener VLANs existentes
VLAN_DATA="$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge configurar mostrar vlan)"

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
    <link rel="stylesheet" href="/cgi-bin/style.cgi">
<meta charset="UTF-8">
<title>Nova VLAN</title>
</head>
<body>
<div class="container">
    <h2>Nova VLAN</h2>
    <div id="errorBox" class="error-box"></div>
EOM

# Pasamos VLAN_DATA a JavaScript
echo "<script>"
echo "let vlansExistents = [];"
while IFS=';' read -r nom vid ipmask gw _; do
    [ -z "$vid" ] && continue
    echo "vlansExistents.push({nom: '$nom', vid: '$vid'});"
done <<< "$VLAN_DATA"

cat <<'EOF'
function validaIP(ip) {
    const regex = /^([0-9]{1,3}\.){3}[0-9]{1,3}(\/[0-9]{1,2})?$/;
    if (!regex.test(ip)) return false;
    let partes = ip.split('/');
    let octets = partes[0].split('.');
    for (let o of octets) {
        if (parseInt(o) < 0 || parseInt(o) > 255) return false;
    }
    if (partes[1] && (parseInt(partes[1]) < 1 || parseInt(partes[1]) > 32)) return false;
    return true;
}

function validarFormulario() {
    let nom = document.forms['vlanForm']['nom'].value.trim();
    let vid = document.forms['vlanForm']['vid'].value.trim();
    let ipmasc = document.forms['vlanForm']['ipmasc'].value.trim();
    let ippe = document.forms['vlanForm']['ippe'].value.trim();
    let errorBox = document.getElementById('errorBox');

    errorBox.style.display = 'none';
    errorBox.innerHTML = '';

    if (!nom || !vid || !ipmasc || !ippe) {
        errorBox.innerHTML += 'Tots els camps són obligatoris.<br>';
        errorBox.style.display = 'block';
        return false;
    }

    if (!/^[0-9]+$/.test(vid)) {
        errorBox.innerHTML += 'El VID ha de ser un número.<br>';
        errorBox.style.display = 'block';
        return false;
    }

    if (!validaIP(ipmasc)) {
        errorBox.innerHTML += 'Format d\'IP/Subxarxa incorrecte.<br>';
        errorBox.style.display = 'block';
        return false;
    }

    if (!validaIP(ippe)) {
        errorBox.innerHTML += 'IP/PE incorrecta.<br>';
        errorBox.style.display = 'block';
        return false;
    }

    for (let v of vlansExistents) {
        if (v.vid === vid) {
            errorBox.innerHTML += 'Ja existeix una VLAN amb el VID ' + vid + '.<br>';
            errorBox.style.display = 'block';
            return false;
        }
        if (v.nom.toLowerCase() === nom.toLowerCase()) {
            errorBox.innerHTML += 'Ja existeix una VLAN amb el nom "' + nom + '".<br>';
            errorBox.style.display = 'block';
            return false;
        }
    }
    return true;
}
</script>
EOF

cat <<'EOF'
    <form name="vlanForm" action="/cgi-bin/bridge-guardar.cgi" method="get" onsubmit="return validarFormulario()">
        <div class="card">
            <div class="card-header"><h3 class="card-title">Dades d'Identificació</h3></div>
            <div class="form-group">
                <label>Nom de la VLAN:</label>
                <input type="text" name="nom" placeholder="Ex: Produccio">
            </div>
            <div class="form-group">
                <label>VLAN ID (VID):</label>
                <input type="text" name="vid" placeholder="Ex: 10">
            </div>
        </div>

        <div class="card">
            <div class="card-header"><h3 class="card-title">Configuració de Xarxa</h3></div>
            <div class="form-group">
                <label>IP / Subxarxa:</label>
                <input type="text" name="ipmasc" placeholder="Ex: 192.168.10.0/24">
            </div>
            <div class="form-group">
                <label>Porta d'enllaç (GW):</label>
                <input type="text" name="ippe" placeholder="Ex: 192.168.10.1">
            </div>
        </div>

        <div class="btn-group">
            <a href="/cgi-bin/bridge-configurar.cgi" class="btn btn-back">⬅Tornar</a>
            <button type="submit" class="btn btn-submit">Crear VLAN</button>
        </div>
    </form>
</div>
</body>
</html>
EOF
