#!/bin/bash

# switch-macs.cgi - Gestió de MACs i Bloquejos

source /usr/local/JSBach/conf/variables.conf
MACS_FILE="$DIR/$PROJECTE/$DIR_CONF/$MACS_SWITCHES_CONF"

# Parse Query String & Post Data
if [ "$REQUEST_METHOD" = "POST" ]; then
    read -n $CONTENT_LENGTH POST_DATA
    
    # Improved decoding function
    decode_url() {
        echo -e "${1//%/\\x}" | sed 's/+/ /g' | xargs
    }
    
    ACTION=$(echo "$POST_DATA" | grep -oP 'action=\K[^&]*')
    ACTION=$(decode_url "$ACTION")
    
    MAC=$(echo "$POST_DATA" | grep -oP 'mac=\K[^&]*')
    MAC=$(decode_url "$MAC")
    
    if [ "$ACTION" == "add_mac" ]; then
        # Strict validation: only colons, 6 pairs of hex
        if [[ "$MAC" =~ ^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$ ]]; then
            MAC=${MAC^^}
            
            # Use client_srv_cli to add MAC safely
            OUTPUT=$(/usr/local/JSBach/scripts/client_srv_cli switch configurar afegir_mac "$MAC" 2>&1)
            if [[ "$OUTPUT" == *"MAC afegida"* ]]; then
                 MSG="MAC afegida correctament: $MAC"
                 TYPE="success"
            elif [[ "$OUTPUT" == *"ja existeix"* ]]; then
                 MSG="La MAC $MAC ja existeix a la llista."
                 TYPE="warning"
            else
                 MSG="Error al guardar la MAC: $OUTPUT"
                 TYPE="error"
            fi
        else
            # Debug: show exact value if validation fails
            MSG="Format de MAC invàlid: '$MAC' (Comprova que useu : com a separador i no hi hagi espais)."
            TYPE="error"
        fi
    elif [ "$ACTION" == "del_mac" ]; then
        OUTPUT=$(/usr/local/JSBach/scripts/client_srv_cli switch configurar eliminar_mac "$MAC" 2>&1)
        MSG="MAC eliminada: $MAC"
        TYPE="success"
    elif [ "$ACTION" == "bloquear" ]; then
        OUTPUT=$(/usr/local/JSBach/scripts/client_srv_cli switch configurar crear_acls 2>&1)
        MSG="Bloqueig aplicat (ACLs creades). <br><pre>$OUTPUT</pre>"
        TYPE="info"
    elif [ "$ACTION" == "desbloquear" ]; then
        OUTPUT=$(/usr/local/JSBach/scripts/client_srv_cli switch configurar eliminar_acls 2>&1)
        MSG="Bloqueig eliminat (ACLs esborrades). <br><pre>$OUTPUT</pre>"
        TYPE="info"
    fi
fi

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
    <link rel="stylesheet" href="/cgi-bin/style.cgi">
<meta charset="UTF-8">
</head>
<body>

<h1>Gestió de Bloquejos MAC</h1>

EOM

if [ ! -z "$MSG" ]; then
    echo "<div class='msg msg-$TYPE'>$MSG</div>"
fi

cat << EOM
<div class="actions-panel">
    <form method="POST" style="margin: 0;">
        <input type="hidden" name="action" value="bloquear">
        <button type="submit" class="btn btn-danger">APLICAR BLOQUEJOS (Crear ACLs)</button>
    </form>
    
    <form method="POST" style="margin: 0;">
        <input type="hidden" name="action" value="desbloquear">
        <button type="submit" class="btn btn-success">TREURE BLOQUEJOS (Esborrar ACLs)</button>
    </form>
</div>

<h3>Afegir Nova MAC a Bloquejar</h3>
<form method="POST" style="background: #1e293b; padding: 20px; border-radius: 8px; display: flex; gap: 10px; align-items: center;">
    <input type="hidden" name="action" value="add_mac">
    <input type="text" name="mac" placeholder="Ex: 00:11:22:33:44:55" class="input-field" required pattern="^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$">
    <button type="submit" class="btn">Afegir a la Llista</button>
</form>

<h3>Llista de MACs Bloquejades</h3>
<table>
    <thead>
        <tr>
            <th>MAC Address</th>
            <th>Accions</th>
        </tr>
    </thead>
    <tbody>
EOM

if [ -f "$MACS_FILE" ]; then
    while read -r line; do
        [[ -z "$line" || "$line" =~ ^# ]] && continue
        echo "<tr>"
        echo "<td style='font-family: monospace; font-size: 1.1em;'>$line</td>"
        echo "<td>"
        echo "<form method='POST' style='margin:0;'>"
        echo "<input type='hidden' name='action' value='del_mac'>"
        echo "<input type='hidden' name='mac' value='$line'>"
        echo "<button type='submit' class='btn btn-danger' style='padding: 5px 10px; font-size: 0.8rem;'>Eliminar</button>"
        echo "</form>"
        echo "</td>"
        echo "</tr>"
    done < "$MACS_FILE"
else
    echo "<tr><td colspan='2'>No hi ha fitxer de MACs configurat.</td></tr>"
fi

echo "</tbody></table></body></html>"
