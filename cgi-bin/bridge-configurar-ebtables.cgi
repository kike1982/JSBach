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
    <link rel="stylesheet" href="/cgi-bin/style.cgi">
<meta charset="utf-8">
<title>Aïllament VLAN</title>
</head>
<body>
    <div class="container">
        <h2>Gestió d'Aïllament VLAN</h2>
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
        ESTAT_TXT="<span class='badge badge-isolated'>AÏLLAT</span>"
        BTN_TXT="Desaillar"
        BTN_ACTION="desaillar"
        BTN_CLASS="btn-unisolate"
    else
        ESTAT_TXT="<span class='badge badge-normal'>NORMAL</span>"
        BTN_TXT="Aillar"
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
