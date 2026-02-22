#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html"
echo ""

# --- Funció per obtenir interfícies Ethernet (sense lo ni wifi) ---
Interfaces_Ethernet() {
    for iface in $(ip -o link show | awk -F': ' '{print $2}'); do
        # Excloure loopback i bridges (br0, br0.X)
        if [[ "$iface" == "lo" || "$iface" == br* ]]; then
            continue
        fi

        # Excloure interfícies wifi
        if iw dev 2>/dev/null | grep -qw "$iface"; then
            continue
        fi

        echo "$iface"
    done
}

CONFIGURACIO=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli ifwan configurar mostrar)
conf_mode=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' '  -f1 )
conf_int=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' '  -f2 )
if [[ "$conf_mode" == "manual" ]]; then
	conf_ip=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' '  -f3 )
	conf_masc=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' '  -f4 )
	conf_pe=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' '  -f5 )
	conf_dns=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' ' -f6 )
fi

# --- Inici HTML ---
cat <<'EOF'
<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="UTF-8">
<title>Configuració WAN</title>
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
legend {
    display: none; /* Usamos card-header en su lugar */
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
}
input[type="text"]:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

/* Custom Radio Buttons */
.radio-group {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
}
.radio-item {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
}
input[type="radio"] {
    accent-color: #3b82f6;
    width: 18px;
    height: 18px;
    cursor: pointer;
}

.btn-submit {
    display: block;
    width: 100%;
    padding: 14px;
    background: #3b82f6;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 700;
    font-size: 1rem;
    transition: all 0.2s;
    text-transform: uppercase;
    letter-spacing: 0.025em;
    margin-top: 32px;
}
.btn-submit:hover {
    background: #2563eb;
    transform: translateY(-1px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
}
.btn-submit:active {
    transform: translateY(0);
}

.hidden { display: none; }
</style>

<script>
function toggleManual() {
    const isManual = document.getElementById("manual").checked;
    const section = document.getElementById("manual-section");
    if (isManual) {
        section.style.display = "block";
        section.classList.remove("hidden");
    } else {
        section.style.display = "none";
        section.classList.add("hidden");
    }
}

function validaIP(ip) {
    const parts = ip.split(".");
    if (parts.length !== 4) return false;
    return parts.every(p => {
        const n = parseInt(p, 10);
        return !isNaN(n) && n >= 0 && n <= 255 && p === n.toString();
    });
}

function validarForm() {
    const modeManual = document.getElementById("manual").checked;
    if (!modeManual) return true;

    const fields = [
        { id: 'ip', name: 'IP' },
        { id: 'masc', name: 'Màscara' },
        { id: 'pe', name: 'Porta d\'enllaç' },
        { id: 'dns', name: 'DNS' }
    ];

    for (const field of fields) {
        const val = document.getElementsByName(field.id)[0].value.trim();
        if (!val) {
            alert(`Falta omplir el camp: ${field.name}`);
            return false;
        }
        if (!validaIP(val)) {
            alert(`El camp ${field.name} no té un format d'IP vàlid.`);
            return false;
        }
    }
    return true;
}

window.addEventListener("DOMContentLoaded", toggleManual);
</script>
</head>
<body>
<div class="container">
    <h2>⚙️ Configuració WAN</h2>

    <form action="/cgi-bin/ifwan-guardar.cgi" method="get" onsubmit="return validarForm()">
        
        <!-- SECCIÓ 1: MODE -->
        <div class="card">
            <div class="card-header">
                <h3 class="card-title">🌐 Mode de configuració</h3>
            </div>
            <div class="radio-group">
EOF

echo "                <label class='radio-item'><input type='radio' id='dhcp' name='mode' value='dhcp' onclick='toggleManual()' $dhcp_check> DHCP</label>"
echo "                <label class='radio-item'><input type='radio' id='manual' name='mode' value='manual' onclick='toggleManual()' $manual_check> Manual</label>"

cat <<'EOF'
            </div>
        </div>

        <!-- SECCIÓ 2: INTERFÍCIES -->
        <div class="card">
            <div class="card-header">
                <h3 class="card-title">🔌 Interfície</h3>
            </div>
            <div class="radio-group">
EOF

for iface in $(Interfaces_Ethernet); do
    checked=""
    [[ "$iface" == "$conf_int" ]] && checked="checked"
    echo "                <label class='radio-item'><input type='radio' name='int' id='$iface' value='$iface' $checked> $iface</label>"
done

cat <<'EOF'
            </div>
        </div>

        <!-- SECCIÓ 3: CONFIGURACIÓ MANUAL -->
        <div id="manual-section" class="card hidden">
            <div class="card-header">
                <h3 class="card-title">📝 Dades de Xarxa</h3>
            </div>
EOF

echo "            <div class='form-group'><label>Adreça IP:</label><input type='text' name='ip' value='' placeholder='Ex: 192.168.1.50'></div>"
echo "            <div class='form-group'><label>Màscara de xarxa:</label><input type='text' name='masc' value='' placeholder='Ex: 255.255.255.0'></div>"
echo "            <div class='form-group'><label>Porta d'enllaç:</label><input type='text' name='pe' value='' placeholder='Ex: 192.168.1.1'></div>"
echo "            <div class='form-group'><label>Servidor DNS:</label><input type='text' name='dns' value='' placeholder='Ex: 8.8.8.8'></div>"

cat <<'EOF'
        </div>

        <button type="submit" class="btn-submit">💾 Guardar Configuració</button>
    </form>
</div>
</body>
</html>
EOF