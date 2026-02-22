#!/bin/bash

# switch-config.cgi - Configuració de Switches

source /usr/local/JSBach/conf/variables.conf

MSG=""
TYPE=""

# Parse Query String & Post Data
if [ "$REQUEST_METHOD" = "POST" ]; then
    read -n $CONTENT_LENGTH POST_DATA
    
    ACTION=$(echo "$POST_DATA" | grep -oP 'action=\K[^&]*')
    ACTION=$(echo -e "${ACTION//%/\\x}" | sed 's/+/ /g')
    
    if [ "$ACTION" == "del_switch" ]; then
        IP=$(echo "$POST_DATA" | grep -oP 'ip=\K[^&]*')
        IP=$(echo -e "${IP//%/\\x}" | sed 's/+/ /g')
        OUTPUT=$(/usr/local/JSBach/scripts/client_srv_cli switch configurar eliminar_switch "$IP" 2>&1)
        MSG="Switch eliminat: $IP"
        TYPE="success"
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

<h1>Configuració de Switches</h1>

EOM

if [ ! -z "$MSG" ]; then
    echo "<div class='msg msg-$TYPE'>$MSG</div>"
fi

cat << EOM

<div class="form-card">
    <h3 style="margin-top:0;">Afegir Nou Switch</h3>
    <form method="POST" action="switch-guardar.cgi">
        <input type="hidden" name="action" value="add_switch">
        
        <div class="input-group">
            <label>Nom del Switch</label>
            <input type="text" name="nom" required placeholder="Ex: sw-planta-1" pattern="^sw.*" title="El nom ha de començar per 'sw'">
        </div>
        
        <div class="input-group">
            <label>Adreça IP</label>
            <input type="text" name="ip" required placeholder="Ex: 192.168.1.10" pattern="^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$" title="Format d'IP vàlid">
        </div>
        
        <div class="input-group">
            <label>Usuari SSH</label>
            <input type="text" name="user" required placeholder="Usuari administrador">
        </div>
        
        <div class="input-group">
            <label>Contrasenya</label>
            <input type="password" name="pass" required placeholder="Contrasenya segura" pattern="^[^$()\`&quot;';&|]*$" title="No es permeten caràcters especials de shell ($ ( ) \` &quot; ' ; & |)">
        </div>
        
        <div class="input-group">
            <label>Protocol (Opcional)</label>
            <select name="proto">
                <option value="ssh">SSH</option>
                <option value="telnet">Telnet</option>
            </select>
        </div>
        
        <button type="submit" class="btn btn-success" style="width: 100%;">Guardar Switch</button>
    </form>
</div>

<h3>Switches Configurats</h3>
<table>
    <thead>
        <tr>
            <th>Nom</th>
            <th>IP</th>
            <th>Usuari</th>
            <th>Protocol</th>
            <th>Accions</th>
        </tr>
    </thead>
    <tbody>
EOM

SWITCHES_FILE="$DIR/$PROJECTE/$DIR_CONF/$SWITCHES_CONF"
if [ -f "$SWITCHES_FILE" ]; then
    while IFS=';' read -r nom ip user pass proto; do
        [[ -z "$nom" || "$nom" =~ ^# ]] && continue
        echo "<tr>"
        echo "<td>$nom</td>"
        echo "<td>$ip</td>"
        echo "<td>$user</td>"
        echo "<td>$proto</td>"
        echo "<td>"
        echo "<form method='POST' style='margin:0;'>"
        echo "<input type='hidden' name='action' value='del_switch'>"
        echo "<input type='hidden' name='ip' value='$ip'>"
        echo "<button type='submit' class='btn btn-danger' style='padding: 5px 10px; font-size: 0.8rem;'>Eliminar</button>"
        echo "</form>"
        echo "</td>"
        echo "</tr>"
    done < "$SWITCHES_FILE"
else
    echo "<tr><td colspan='5'>No hi ha switches configurats.</td></tr>"
fi

echo "</tbody></table></body></html>"
