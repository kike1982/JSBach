#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
    <link rel="stylesheet" href="/cgi-bin/style.cgi">
  <meta charset="utf-8">
  <title>Tallafocs Configuració Input</title>
</head>
<body>
<div class="container">
    <h2>Regles d'Entrada (INPUT)</h2>
EOM

# --- WAN SECTION ---
echo "<h3>INTERNET INPUT (WAN)</h3>"
estat_wan=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs estat_wan 0)

echo "<div class='card'>"
echo "  <div class='status-row'>"
if [ "$estat_wan" == "NO_WAN" ]; then
    echo "    <div class='info-group'><span class='label'>WAN No configurada</span></div>"
else
    echo "    <div class='info-group'>"
    echo "      <span class='label'>Accés des de l'Exterior</span>"
    echo "      <span class='sublabel'>Estat actual: $estat_wan</span>"
    echo "    </div>"
    
    if [ "$estat_wan" == "BLOCKED" ]; then
        echo "    <span class='badge badge-blocked'>BLOQUEJAT</span>"
        echo "    <a href='tallafocs-input-action.cgi?accio=desbloquejar_internet&id=0' class='btn btn-connect'>Desbloquejar</a>"
    else
        echo "    <span class='badge badge-open'>OBERT</span>"
        echo "    <a href='tallafocs-input-action.cgi?accio=bloquejar_internet&id=0' class='btn btn-disconnect'>Bloquejar + No Ping</a>"
    fi
fi
echo "  </div>"
echo "</div>"

# --- VLAN SECTION ---
echo "<h3>INPUT PER VLAN</h3>"

for linia in $(grep -v '#' "$DIR/$PROJECTE/$DIR_CONF/$BRIDGE_CONF"); do
    nom=$(echo "$linia"|cut -d';' -f1)
    id=$(echo "$linia"|cut -d';' -f2)
    ip=$(echo "$linia"|cut -d';' -f3)

    estat_input=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs estat_input $id)

    case "$estat_input" in
        "CONNECTADA") BADGE_CLASS="badge-open"; ICON="";;
        "DESCONNECTADA") BADGE_CLASS="badge-blocked"; ICON="";;
        *) BADGE_CLASS="badge-blocked"; ICON="";;
    esac

    echo "<div class='card'>"
    echo "  <div class='status-row'>"
    echo "    <div class='info-group'>"
    echo "      <span class='label'>$nom</span>"
    echo "      <span class='sublabel'>ID: $id | $ip</span>"
    echo "    </div>"
    echo "    <span class='badge $BADGE_CLASS'>$ICON $estat_input</span>"
    
    if [ "$estat_input" == "CONNECTADA" ]; then
        echo "    <a href='tallafocs-input-action.cgi?id=$id&accio=input_desconnectar' class='btn btn-disconnect'>Desconnectar Input</a>"
    else
        echo "    <a href='tallafocs-input-action.cgi?id=$id&accio=input_connectar' class='btn btn-connect'>Connectar Input</a>"
    fi
    echo "  </div>"
    echo "</div>"
done

cat << EOM
</div>
</body>
</html>
EOM
