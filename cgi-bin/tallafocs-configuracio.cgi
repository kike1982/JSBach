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
  <title>Tallafocs Configuració</title>
</head>
<body>
<div class="container">
    <h2>🛡️ Configuració Tallafocs</h2>
    
    <h3>📶 ESTAT DE LES VLANS</h3>
EOM

for linia in $(grep -v '#' "$DIR/$PROJECTE/$DIR_CONF/$BRIDGE_CONF"); do
    nom=$(echo "$linia"|cut -d';' -f1)
    id=$(echo "$linia"|cut -d';' -f2)
    ip=$(echo "$linia"|cut -d';' -f3)
    estat_vlan=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs estat $id)

    case "$estat_vlan" in
        "CONNECTADA") BADGE_CLASS="badge-conn";;
        "DESCONNECTADA") BADGE_CLASS="badge-desconn";;
        "CONNECTADA PORT WLS") BADGE_CLASS="badge-wls";;
        "AILLADA") BADGE_CLASS="badge-ailla";;
        *) BADGE_CLASS="badge-desconn";;
    esac

    echo "<div class='card'>"
    echo "  <div class='vlan-row'>"
    echo "    <div class='vlan-info'>"
    echo "      <span class='vlan-name'>$nom</span>"
    echo "      <span class='vlan-net'>ID: $id | $ip</span>"
    echo "    </div>"
    echo "    <span class='badge $BADGE_CLASS'>$estat_vlan</span>"
    echo "    <div class='btn-group'>"
    
    case "$estat_vlan" in
        "CONNECTADA")
            echo "<a href='tallafocs-conndeconn.cgi?id=$id&accio=desconnectar' class='btn btn-danger'>🔌 Tallar</a>"
            echo "<a href='tallafocs-conndeconn.cgi?id=$id&accio=connectar_port_wls' class='btn btn-warning'>🌐 Ports WLS</a>"
            echo "<a href='tallafocs-conndeconn.cgi?id=$id&accio=aillar' class='btn btn-danger'>🔒 Aïllar</a>"
            ;;
        "DESCONNECTADA")
            echo "<a href='tallafocs-conndeconn.cgi?id=$id&accio=connectar' class='btn btn-success'>🔗 Connectar</a>"
            echo "<a href='tallafocs-conndeconn.cgi?id=$id&accio=connectar_port_wls' class='btn btn-warning'>🌐 Ports WLS</a>"
            echo "<a href='tallafocs-conndeconn.cgi?id=$id&accio=aillar' class='btn btn-danger'>🔒 Aïllar</a>"
            ;;
        "CONNECTADA PORT WLS")
            echo "<a href='tallafocs-conndeconn.cgi?id=$id&accio=desconnectar' class='btn btn-danger'>🔌 Tallar</a>"
            echo "<a href='tallafocs-conndeconn.cgi?id=$id&accio=connectar' class='btn btn-success'>🔗 Full Internet</a>"
            echo "<a href='tallafocs-conndeconn.cgi?id=$id&accio=aillar' class='btn btn-danger'>🔒 Aïllar</a>"
            ;;
        "AILLADA")
            echo "<a href='tallafocs-conndeconn.cgi?id=$id&accio=desconnectar' class='btn btn-danger'>🔌 Tallar</a>"
            echo "<a href='tallafocs-conndeconn.cgi?id=$id&accio=connectar' class='btn btn-success'>🔗 Connectar</a>"
            echo "<a href='tallafocs-conndeconn.cgi?id=$id&accio=desaillar' class='btn btn-success'>🔓 Desaïllar</a>"
            ;;
    esac

    echo "    </div>"
    echo "  </div>"
    echo "</div>"
done

echo "<h3>📝 WHITELIST PORTS</h3>"
echo "<div class='card'>"
echo "  <table>"
echo "    <thead><tr><th>Protocol</th><th>Port</th><th style='text-align:right'>Accions</th></tr></thead>"
echo "    <tbody>"

for linia in $(grep -v '#' "$DIR/$PROJECTE/$DIR_CONF/$PORTS_WLS"); do
    PROTOCOL=$(echo "$linia"|cut -d';' -f1)
    PORT=$(echo "$linia"|cut -d';' -f2)
    echo "<tr>"
    echo "  <td><span class='badge badge-wls'>$PROTOCOL</span></td>"
    echo "  <td><strong>$PORT</strong></td>"
    echo "  <td style='text-align:right'><a href='tallafocs-ports-wls.cgi?accio=eliminar_port_wls&protocol=$PROTOCOL&port=$PORT' class='btn btn-danger'>🗑️ Eliminar</a></td>"
    echo "</tr>"
done

echo "    </tbody>"
echo "  </table>"
echo "  <div class='add-section'><a href='tallafocs-nova-port-wls.cgi' class='btn btn-success'>➕ Afegir Port</a></div>"
echo "</div>"

echo "<h3>🏢 IPS AMB ACCÉS PERSONALITZAT</h3>"
echo "<div class='card'>"
echo "  <table>"
echo "    <thead><tr><th>VID</th><th>IP</th><th>MAC</th><th style='text-align:right'>Accions</th></tr></thead>"
echo "    <tbody>"

for linia in $(grep -v '#' "$DIR/$PROJECTE/$DIR_CONF/$IPS_WLS"); do
    VID=$(echo "$linia"|cut -d';' -f1)
    IP=$(echo "$linia"|cut -d';' -f2)
    MAC=$(echo "$linia"|cut -d';' -f3)
    echo "<tr>"
    echo "  <td><span class='badge badge-conn'>$VID</span></td>"
    echo "  <td><strong>$IP</strong></td>"
    echo "  <td><code style='color:#94a3b8'>$MAC</code></td>"
    echo "  <td style='text-align:right'><a href='tallafocs-ips-wls.cgi?accio=eliminar_ip_wls&vid=$VID&ip=$IP&mac=$MAC' class='btn btn-danger'>🗑️ Eliminar</a></td>"
    echo "</tr>"
done

echo "    </tbody>"
echo "  </table>"
echo "  <div class='add-section'><a href='tallafocs-nova-ip-wls.cgi' class='btn btn-success'>➕ Afegir IP</a></div>"
echo "</div>"

cat << EOM
</div>
</body>
</html>
EOM
