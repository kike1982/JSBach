#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
  <meta charset="utf-8">
  <title>Tallafocs Configuració Input</title>
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
    .status-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 20px;
        flex-wrap: wrap;
    }
    .info-group {
        display: flex;
        flex-direction: column;
    }
    .label { font-weight: 700; color: #f8fafc; font-size: 1.1rem; }
    .sublabel { font-family: 'Fira Code', monospace; color: #94a3b8; font-size: 0.85rem; }
    
    .badge {
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 800;
        text-transform: uppercase;
    }
    .badge-open { background: rgba(16, 185, 129, 0.1); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.2); }
    .badge-blocked { background: rgba(239, 68, 68, 0.1); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.2); }

    .btn {
        padding: 8px 14px;
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
        gap: 8px;
    }
    .btn-connect { background: #10b981; color: white; }
    .btn-connect:hover { background: #059669; transform: translateY(-1px); }
    .btn-disconnect { background: #ef4444; color: white; }
    .btn-disconnect:hover { background: #dc2626; transform: translateY(-1px); }
  </style>
</head>
<body>
<div class="container">
    <h2>📥 Regles d'Entrada (INPUT)</h2>
EOM

# --- WAN SECTION ---
echo "<h3>🌐 INTERNET INPUT (WAN)</h3>"
estat_wan=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs estat_wan 0)

echo "<div class='card'>"
echo "  <div class='status-row'>"
if [ "$estat_wan" == "NO_WAN" ]; then
    echo "    <div class='info-group'><span class='label'>⚠️ WAN No configurada</span></div>"
else
    echo "    <div class='info-group'>"
    echo "      <span class='label'>Accés des de l'Exterior</span>"
    echo "      <span class='sublabel'>Estat actual: $estat_wan</span>"
    echo "    </div>"
    
    if [ "$estat_wan" == "BLOCKED" ]; then
        echo "    <span class='badge badge-blocked'>🔒 BLOQUEJAT</span>"
        echo "    <a href='tallafocs-input-action.cgi?accio=desbloquejar_internet&id=0' class='btn btn-connect'>🔓 Desbloquejar</a>"
    else
        echo "    <span class='badge badge-open'>🔓 OBERT</span>"
        echo "    <a href='tallafocs-input-action.cgi?accio=bloquejar_internet&id=0' class='btn btn-disconnect'>🔒 Bloquejar + No Ping</a>"
    fi
fi
echo "  </div>"
echo "</div>"

# --- VLAN SECTION ---
echo "<h3>📶 INPUT PER VLAN</h3>"

for linia in $(grep -v '#' "$DIR/$PROJECTE/$DIR_CONF/$BRIDGE_CONF"); do
    nom=$(echo "$linia"|cut -d';' -f1)
    id=$(echo "$linia"|cut -d';' -f2)
    ip=$(echo "$linia"|cut -d';' -f3)

    estat_input=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs estat_input $id)

    case "$estat_input" in
        "CONNECTADA") BADGE_CLASS="badge-open"; ICON="🔓";;
        "DESCONNECTADA") BADGE_CLASS="badge-blocked"; ICON="🔒";;
        *) BADGE_CLASS="badge-blocked"; ICON="❓";;
    esac

    echo "<div class='card'>"
    echo "  <div class='status-row'>"
    echo "    <div class='info-group'>"
    echo "      <span class='label'>$nom</span>"
    echo "      <span class='sublabel'>ID: $id | $ip</span>"
    echo "    </div>"
    echo "    <span class='badge $BADGE_CLASS'>$ICON $estat_input</span>"
    
    if [ "$estat_input" == "CONNECTADA" ]; then
        echo "    <a href='tallafocs-input-action.cgi?id=$id&accio=input_desconnectar' class='btn btn-disconnect'>🔒 Desconnectar Input</a>"
    else
        echo "    <a href='tallafocs-input-action.cgi?id=$id&accio=input_connectar' class='btn btn-connect'>🔗 Connectar Input</a>"
    fi
    echo "  </div>"
    echo "</div>"
done

cat << EOM
</div>
</body>
</html>
EOM
