#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

int=$(echo "$QUERY_STRING" | sed -n 's/^.*int=\([^&]*\).*$/\1/p')

VLAN_DATA="$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge configurar mostrar bridge)"
linia_int=$(echo "$VLAN_DATA" | grep -E "^${int};")
VLAN_UNTAG=$(echo "$linia_int" | cut -d';' -f2)
VLAN_TAG=$(echo "$linia_int" | cut -d';' -f3)

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
    <link rel="stylesheet" href="/cgi-bin/style.cgi">
    <meta charset="utf-8">
    <title>Modificar Tag-Untag</title>
</head>
<body>
    <div class="container">
        <h2>Modificar Tag-Untag</h2>
        <form action='/cgi-bin/bridge-guardar-taguntag.cgi' method='get'>
            <div class="card">
                <div class="card-header"><h3 class="card-title">Interfaç de Xarxa</h3></div>
                <div class="form-group">
                    <label>Nom de l'interfaç:</label>
                    <input type="text" name="int" value="$int" readonly>
                </div>
            </div>

            <div class="card">
                <div class="card-header"><h3 class="card-title">Configuració VLAN</h3></div>
                <div class="form-group">
                    <label>VLAN UNTAG (PVID):</label>
                    <input type="text" name="untag" value="$VLAN_UNTAG" 
                           pattern="^[0-9]+$" required 
                           title="Només números. 0 si no hi ha VLAN untagged.">
                </div>
                <div class="form-group">
                    <label>VLANs TAGGED:</label>
                    <input type="text" name="tag" value="$VLAN_TAG" 
                           pattern="^[0-9]+(-[0-9]+)?(,[0-9]+(-[0-9]+)?)*$" required
                           title="Llista de VLANs. Exemple: 10,20 o rangs 10-20 o combinat 10-20,30,40-45">
                </div>
            </div>

            <div class="btn-group">
                <a href="/cgi-bin/bridge-configurar-taguntag.cgi" class="btn btn-back">⬅Tornar</a>
                <button type="submit" class="btn btn-submit">Guardar Canvis</button>
            </div>
        </form>
        <div class='footer'>Gestió de xarxes © 2026</div>
    </div>
</body>
</html>
EOM
