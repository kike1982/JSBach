#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
  <meta charset="utf-8">
  <title>Tallafocs Configuració</title>
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
        max-width: 1000px;
        margin: 0 auto;
    }
    h2, h3 {
        color: #3b82f6;
        margin-bottom: 24px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    h3 {
        font-size: 1.25rem;
        border-left: 4px solid #3b82f6;
        padding-left: 15px;
        margin-top: 40px;
    }
    .card {
        background: #1e293b;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    .vlan-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 20px;
        flex-wrap: wrap;
    }
    .vlan-info {
        display: flex;
        flex-direction: column;
    }
    .vlan-name { font-weight: 700; color: #f8fafc; font-size: 1.1rem; }
    .vlan-net { font-family: 'Fira Code', monospace; color: #94a3b8; font-size: 0.85rem; }
    
    .badge {
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 800;
        text-transform: uppercase;
    }
    .badge-conn { background: rgba(16, 185, 129, 0.1); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.2); }
    .badge-desconn { background: rgba(100, 116, 139, 0.1); color: #94a3b8; border: 1px solid rgba(100, 116, 139, 0.2); }
    .badge-wls { background: rgba(59, 130, 246, 0.1); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.2); }
    .badge-ailla { background: rgba(239, 68, 68, 0.1); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.2); }

    .btn-group {
        display: flex;
        gap: 8px;
    }
    .btn {
        padding: 8px 12px;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-weight: 700;
        font-size: 0.8rem;
        transition: all 0.2s;
        text-transform: uppercase;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    .btn-primary { background: #3b82f6; color: white; }
    .btn-primary:hover { background: #2563eb; transform: translateY(-1px); }
    .btn-danger { background: #ef4444; color: white; }
    .btn-danger:hover { background: #dc2626; transform: translateY(-1px); }
    .btn-success { background: #10b981; color: white; }
    .btn-success:hover { background: #059669; transform: translateY(-1px); }
    .btn-warning { background: #f59e0b; color: white; }
    .btn-warning:hover { background: #d97706; transform: translateY(-1px); }

    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
    }
    th {
        text-align: left;
        color: #64748b;
        padding: 12px 14px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        font-size: 0.8rem;
        text-transform: uppercase;
    }
    td {
        padding: 14px;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        color: #cbd5e1;
    }
    .add-section {
        margin-top: 20px;
        display: flex;
        justify-content: flex-end;
    }
  </style>
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
