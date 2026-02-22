#!/bin/bash

# switch-guardar.cgi - Processar i Guardar Nous Switches

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

MSG=""
TYPE=""
NOM=""
IP=""
USER=""
PASS=""
PROTO=""

# Parse Post Data
if [ "$REQUEST_METHOD" = "POST" ]; then
    read -n $CONTENT_LENGTH POST_DATA
    
    ACTION=$(echo "$POST_DATA" | grep -oP 'action=\K[^&]*')
    ACTION=$(echo -e "${ACTION//%/\\x}" | sed 's/+/ /g')
    
    if [ "$ACTION" == "add_switch" ]; then
        NOM=$(echo "$POST_DATA" | grep -oP 'nom=\K[^&]*')
        NOM=$(echo -e "${NOM//%/\\x}" | sed 's/+/ /g')
        
        IP=$(echo "$POST_DATA" | grep -oP 'ip=\K[^&]*')
        IP=$(echo -e "${IP//%/\\x}" | sed 's/+/ /g')
        
        USER=$(echo "$POST_DATA" | grep -oP 'user=\K[^&]*')
        USER=$(echo -e "${USER//%/\\x}" | sed 's/+/ /g')
        
        PASS=$(echo "$POST_DATA" | grep -oP 'pass=\K[^&]*')
        PASS=$(echo -e "${PASS//%/\\x}" | sed 's/+/ /g')
        
        PROTO=$(echo "$POST_DATA" | grep -oP 'proto=\K[^&]*')
        PROTO=$(echo -e "${PROTO//%/\\x}" | sed 's/+/ /g')
        
        # Executar backend amb validacions completes
        OUTPUT=$(/usr/local/JSBach/scripts/client_srv_cli switch configurar afegir_switch "$NOM" "$IP" "$USER" "$PASS" "$PROTO" 2>&1)
        
        if echo "$OUTPUT" | grep -q "afegit correctament"; then
            MSG="Switch afegit correctament."
            TYPE="success"
        else
            # Extreure l'error del backend
            MSG=$(echo "$OUTPUT" | grep -oP '❌ ERROR: \K.*')
            [ -z "$MSG" ] && MSG=$(echo "$OUTPUT" | grep -oP '⚠️ \K.*')
            [ -z "$MSG" ] && MSG="Error desconegut al guardar el switch."
            TYPE="error"
        fi
    fi
fi

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="3;url=$SWITCH_CONFIG_CGI">
<style>
body { background: #0f172a; font-family: 'Inter', sans-serif; color: #f8fafc; padding: 40px; text-align: center; }
.card { background: #1e293b; padding: 40px; border-radius: 12px; border: 1px solid #334155; max-width: 600px; margin: 0 auto; }
h1 { color: #10b981; margin-top: 0; }
.error { color: #ef4444; }
.details { text-align: left; background: rgba(0,0,0,0.2); padding: 20px; border-radius: 8px; margin-top: 20px; }
.btn { background: #3b82f6; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; text-decoration: none; display: inline-block; margin-top: 20px; }
.btn:hover { background: #2563eb; }
</style>
</head>
<body>

<div class="card">
EOM

if [ "$TYPE" == "success" ]; then
    echo "<h1>✅ $MSG</h1>"
    echo "<div class='details'>"
    echo "<p><strong>Nom:</strong> $NOM</p>"
    echo "<p><strong>IP:</strong> $IP</p>"
    echo "<p><strong>Usuari:</strong> $USER</p>"
    echo "<p><strong>Protocol:</strong> $PROTO</p>"
    echo "</div>"
    echo "<p>Redirigint en 3 segons...</p>"
else
    echo "<h1 class='error'>❌ Error</h1>"
    echo "<p>$MSG</p>"
    echo "<div class='details'><pre>$OUTPUT</pre></div>"
    echo "<p><a href='$SWITCH_CONFIG_CGI' class='btn'>Tornar a intentar</a></p>"
fi

echo "</div></body></html>"
