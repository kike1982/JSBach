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
<meta charset="UTF-8">
<title>Nova VLAN</title>
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
    color: #10b981;
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
    border-color: #10b981;
    box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2);
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
.btn-submit { background: #10b981; color: white; }
.btn-submit:hover { background: #059669; transform: translateY(-1px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3); }
.btn-back { background: #475569; color: white; }
.btn-back:hover { background: #334155; transform: translateY(-1px); }

.error-box {
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
    <h2>✨ Nova VLAN</h2>
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
        errorBox.innerHTML += '⚠️ Tots els camps són obligatoris.<br>';
        errorBox.style.display = 'block';
        return false;
    }

    if (!/^[0-9]+$/.test(vid)) {
        errorBox.innerHTML += '⚠️ El VID ha de ser un número.<br>';
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

    for (let v of vlansExistents) {
        if (v.vid === vid) {
            errorBox.innerHTML += '⚠️ Ja existeix una VLAN amb el VID ' + vid + '.<br>';
            errorBox.style.display = 'block';
            return false;
        }
        if (v.nom.toLowerCase() === nom.toLowerCase()) {
            errorBox.innerHTML += '⚠️ Ja existeix una VLAN amb el nom "' + nom + '".<br>';
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
            <div class="card-header"><h3 class="card-title">📝 Dades d'Identificació</h3></div>
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
            <div class="card-header"><h3 class="card-title">🌐 Configuració de Xarxa</h3></div>
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
            <a href="/cgi-bin/bridge-configurar.cgi" class="btn btn-back">⬅️ Tornar</a>
            <button type="submit" class="btn btn-submit">🚀 Crear VLAN</button>
        </div>
    </form>
</div>
</body>
</html>
EOF
