#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

# ---------------------------------------------------------------
# 1. Processar accions (si n'hi ha)
# ---------------------------------------------------------------
# Parseig simple de QUERY_STRING: vlan=X&action=aillar/desaillar
VLAN_ID=$(echo "$QUERY_STRING" | grep -oE 'vlan=[0-9]+' | cut -d= -f2)
ACTION=$(echo "$QUERY_STRING" | grep -oE 'action=(aillar|desaillar)' | cut -d= -f2)

if [ -n "$VLAN_ID" ] && [ -n "$ACTION" ]; then
    # Executem l'acció a través del wrapper sudo
    "$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge "$ACTION" "$VLAN_ID" > /dev/null
    
    # Petita pausa per assegurar que s'aplica abans de rellegir l'estat
    sleep 1
fi

# ---------------------------------------------------------------
# 2. Obtenir dades per a la vista
# ---------------------------------------------------------------
# Llegim l'estat d'aïllament específic (VLAN_ID:STATUS)
ISOL_STATUS_RAW=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge isol_status)

# ---------------------------------------------------------------
# 3. Generar HTML
# ---------------------------------------------------------------
echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="utf-8">
<title>Aïllament VLAN</title>
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
    margin-top: 20px;
    margin-bottom: 30px;
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
    padding: 12px 14px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    font-size: 0.85rem;
    text-transform: uppercase;
}
td {
    padding: 16px 14px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    color: #f1f5f9;
}
.badge {
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 800;
    text-transform: uppercase;
}
.badge-isolated { background: rgba(239, 68, 68, 0.1); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.2); }
.badge-normal { background: rgba(16, 185, 129, 0.1); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.2); }

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
    gap: 8px;
}
.btn-isolate { background: #ef4444; color: white; }
.btn-isolate:hover { background: #dc2626; transform: translateY(-1px); }
.btn-unisolate { background: #10b981; color: white; }
.btn-unisolate:hover { background: #059669; transform: translateY(-1px); }

.vlan-name { font-weight: 700; color: #3b82f6; }
.vlan-vid { font-family: monospace; background: rgba(255,255,255,0.05); padding: 2px 6px; border-radius: 4px; }
</style>
</head>
<body>
    <div class="container">
        <h2>🛡️ Gestió d'Aïllament VLAN</h2>
        <div class="card">
            <table>
                <thead>
                    <tr>
                        <th>VLAN Nom</th>
                        <th>VLAN ID</th>
                        <th>IP/Màscara</th>
                        <th>Estat</th>
                        <th>Acció</th>
                    </tr>
                </thead>
                <tbody>
EOM

# Llegim bridge.conf per iterar les VLANs
# Format: vlan_nom;vlan_id;ip/masc;ip_PE;
while IFS=';' read -r NOM VID IP_MASC _ ; do
    # Saltem línies buides o comentaris
    [[ "$NOM" =~ ^# ]] && continue
    [ -z "$VID" ] && continue

    # Determinem l'estat mirant si la línia VID:ISOLATED existeix a la sortida
    if echo "$ISOL_STATUS_RAW" | grep -q "^${VID}:ISOLATED"; then
        ESTAT_TXT="<span class='badge badge-isolated'>🔒 AÏLLAT</span>"
        BTN_TXT="🔓 Desaillar"
        BTN_ACTION="desaillar"
        BTN_CLASS="btn-unisolate"
    else
        ESTAT_TXT="<span class='badge badge-normal'>🔓 NORMAL</span>"
        BTN_TXT="🔒 Aillar"
        BTN_ACTION="aillar"
        BTN_CLASS="btn-isolate"
    fi

    echo "<tr>"
    echo "  <td><span class='vlan-name'>$NOM</span></td>"
    echo "  <td><span class='vlan-vid'>$VID</span></td>"
    echo "  <td>$IP_MASC</td>"
    echo "  <td>$ESTAT_TXT</td>"
    echo "  <td><a href='bridge-configurar-ebtables.cgi?vlan=$VID&action=$BTN_ACTION' class='btn $BTN_CLASS'>$BTN_TXT</a></td>"
    echo "</tr>"

done < "$DIR/$PROJECTE/$DIR_CONF/$BRIDGE_CONF"

cat << EOM
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
EOM
