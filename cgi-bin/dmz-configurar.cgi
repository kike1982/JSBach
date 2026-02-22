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
    <link rel="stylesheet" href="/cgi-bin/style.cgi">
  <meta charset="utf-8">
  <title>Configuració DMZ</title>
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
