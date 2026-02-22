#!/bin/bash

source /usr/local/JSBach/conf/variables.conf
source $DIR/$PROJECTE/$DIR_CONF/$CONF_IFWAN

Interfaces_Ethernet() {
    for iface in $(ip -o link show | awk -F': ' '{print $2}'); do
        if [[ "$iface" != "lo" ]] && [[ "$iface" != "$IFW_IFWAN" ]] && [[ $iface != br0* ]]; then
            if ! iw dev 2>/dev/null | grep -qw "$iface"; then
                echo "$iface"
            fi
        fi
    done
}

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
  <meta charset="utf-8">
  <title>Configuració DMZ</title>
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
    .card {
        background: #1e293b;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
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
    tr:hover {
        background: rgba(255,255,255,0.02);
    }
    .badge {
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 800;
        text-transform: uppercase;
    }
    .badge-proto { background: rgba(59, 130, 246, 0.1); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.2); }
    
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
    .btn-danger { background: #ef4444; color: white; }
    .btn-danger:hover { background: #dc2626; transform: translateY(-1px); }
    .btn-success { background: #10b981; color: white; padding: 12px 24px; font-size: 0.9rem; }
    .btn-success:hover { background: #059669; transform: translateY(-2px); }
    
    .header-actions {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 24px;
    }
    code {
        font-family: 'Fira Code', monospace;
        background: rgba(0,0,0,0.3);
        padding: 2px 6px;
        border-radius: 4px;
        color: #3b82f6;
    }
  </style>
</head>
<body>
<div class="container">
    <div class="header-actions">
        <h2>🌐 Configuració DMZ</h2>
        <a href="/cgi-bin/dmz-nou-servei.cgi" class="btn btn-success">➕ Obrir nou servei</a>
    </div>

    <div class="card">
        <table>
            <thead>
                <tr>
                    <th>Port</th>
                    <th>Protocol</th>
                    <th>IP Servidor</th>
                    <th style="text-align:right">Accions</th>
                </tr>
            </thead>
            <tbody>
EOM

# --- Leer DMZ datos correctamente línea por línea ---
"$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dmz configurar mostrar | while read -r line; do
    # Ignorar líneas vacías y comentarios y el encabezado
    [[ -z "$line" || "$line" =~ ^# || "$line" =~ ^Port ]] && continue

    # Separar campos
    PORT=$(echo "$line" | cut -d';' -f1 | xargs)
    PROTO=$(echo "$line" | cut -d';' -f2 | xargs)
    IP_DMZ=$(echo "$line" | cut -d';' -f3 | xargs)

    echo "<tr>"
    echo "  <td><strong style='color:#f8fafc'>$PORT</strong></td>"
    echo "  <td><span class='badge badge-proto'>$PROTO</span></td>"
    echo "  <td><code>$IP_DMZ</code></td>"
    echo "  <td style='text-align:right'>"
    echo "    <a href='/cgi-bin/dmz-eliminar.cgi?port=$PORT&proto=$PROTO&ipdmz=$IP_DMZ' class='btn btn-danger'>🗑️ Eliminar</a>"
    echo "  </td>"
    echo "</tr>"
done

cat << EOM
            </tbody>
        </table>
    </div>
</div>
</body>
</html>
EOM
