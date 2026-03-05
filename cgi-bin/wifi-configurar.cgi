#!/bin/bash

source /usr/local/JSBach/conf/variables.conf
source "$DIR/$PROJECTE/$DIR_CONF/$WIFI_CONF"

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
    <link rel="stylesheet" href="/cgi-bin/style.cgi">
    <meta charset="utf-8">
    <title>Configuració WiFi AP</title>
</head>
<body>
<div class="container">

    <!-- Configuració de xarxa -->
    <div class="card">
        <h2>⚙️ Configuració de la xarxa WiFi</h2>
        <form action="/cgi-bin/wifi-guardar-xarxa.cgi" method="get">
            <div class="grid grid-2">
                <div class="form-group">
                    <label>SSID (nom de la xarxa)</label>
                    <input type="text" name="ssid" value="$WIFI_SSID" required maxlength="32">
                </div>
                <div class="form-group">
                    <label>Contrasenya (mínim 8 caràcters)</label>
                    <input type="text" name="pass" value="$WIFI_PASSWORD" required minlength="8">
                </div>
                <div class="form-group">
                    <label>Canal WiFi (1-13)</label>
                    <input type="number" name="channel" value="$WIFI_CHANNEL" min="1" max="13" required>
                </div>
                <div class="form-group">
                    <label>IP del punt d'accés</label>
                    <input type="text" name="ip" value="$WIFI_IP" pattern="^([0-9]{1,3}\.){3}[0-9]{1,3}$" required>
                </div>
                <div class="form-group">
                    <label>Prefix de xarxa (CIDR, ex: 24)</label>
                    <input type="number" name="prefix" value="$WIFI_PREFIX" min="8" max="30" required>
                </div>
                <div class="form-group">
                    <label>DHCP inici</label>
                    <input type="text" name="dhcp_start" value="$WIFI_DHCP_START" pattern="^([0-9]{1,3}\.){3}[0-9]{1,3}$" required>
                </div>
                <div class="form-group">
                    <label>DHCP fi</label>
                    <input type="text" name="dhcp_end" value="$WIFI_DHCP_END" pattern="^([0-9]{1,3}\.){3}[0-9]{1,3}$" required>
                </div>
            </div>
            <div class="btn-group">
                <button type="submit" class="btn btn-primary">Guardar configuració</button>
            </div>
        </form>
    </div>

    <!-- Taula de clients MAC -->
    <div class="card">
        <div class="header-actions">
            <h2>🖥️ Clients WiFi (control per MAC)</h2>
            <a href="/cgi-bin/wifi-nou-client.cgi" class="btn btn-success">Afegir client</a>
        </div>
        <table>
            <thead>
                <tr>
                    <th>MAC</th>
                    <th>IP Fixa</th>
                    <th>Nom</th>
                    <th>Estat</th>
                    <th class="text-right">Accions</th>
                </tr>
            </thead>
            <tbody>
EOM

"$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli wifi configurar mostrar | while read -r line; do
    [[ -z "$line" || "$line" =~ ^# || "$line" =~ ^MAC ]] && continue

    MAC=$(echo "$line" | cut -d';' -f1 | xargs)
    IP=$(echo "$line" | cut -d';' -f2 | xargs)
    NOM=$(echo "$line" | cut -d';' -f3 | xargs)
    ESTAT=$(echo "$line" | cut -d';' -f4 | xargs)

    if [[ "$ESTAT" == "BLOQUEJAT" ]]; then
        BADGE_CLASS="badge badge-err"
        BTN_BLOC="<a href='/cgi-bin/wifi-bloc.cgi?mac=$MAC&accio=desbloquejar' class='btn btn-success'>Desbloquejar</a>"
    else
        BADGE_CLASS="badge badge-ok"
        BTN_BLOC="<a href='/cgi-bin/wifi-bloc.cgi?mac=$MAC&accio=bloquejar' class='btn btn-danger'>Bloquejar</a>"
    fi

    echo "<tr>"
    echo "  <td><code>$MAC</code></td>"
    echo "  <td><code>$IP</code></td>"
    echo "  <td><strong style='color:#f8fafc'>$NOM</strong></td>"
    echo "  <td><span class='$BADGE_CLASS'>$ESTAT</span></td>"
    echo "  <td class='text-right'>"
    echo "    $BTN_BLOC"
    echo "    <a href='/cgi-bin/wifi-eliminar.cgi?mac=$MAC' class='btn btn-danger'>Eliminar</a>"
    echo "  </td>"
    echo "</tr>"
done

cat << EOM
            </tbody>
        </table>
    </div>

    <!-- Clients connectats ara mateix -->
    <div class="card">
        <h2>📡 Clients connectats ara mateix</h2>
        <table>
            <thead>
                <tr>
                    <th>MAC</th>
                    <th>IP</th>
                    <th>Nom</th>
                    <th>Senyal</th>
                    <th>Estat</th>
                </tr>
            </thead>
            <tbody>
EOM

# Obtenir MACs associades al AP (connectades ara)
declare -A SIGNAL_MAP
while IFS= read -r line; do
    if [[ "$line" =~ ^Station[[:space:]]([0-9a-f:]{17}) ]]; then
        CURRENT_MAC="${BASH_REMATCH[1]}"
        SIGNAL_MAP["$CURRENT_MAC"]="?"
    elif [[ -n "$CURRENT_MAC" && "$line" =~ signal:[[:space:]]+(-?[0-9]+) ]]; then
        SIGNAL_MAP["$CURRENT_MAC"]="${BASH_REMATCH[1]} dBm"
    fi
done < <(iw dev "$WIFI_IF" station dump 2>/dev/null)

# Llegir leases dnsmasq i mostrar fila per cada una
LEASES_FILE="/var/lib/misc/dnsmasq.leases"
NOW=$(date +%s)
HAS_ROWS=0

if [ -f "$LEASES_FILE" ]; then
    while read -r expiry mac ip nom _; do
        [[ -z "$mac" ]] && continue
        HAS_ROWS=1
        NOM_SHOW="${nom:-sense nom}"
        [ "$NOM_SHOW" = "*" ] && NOM_SHOW="sense nom"

        if [[ -n "${SIGNAL_MAP[$mac]+x}" ]]; then
            ESTAT_BADGE="<span class='badge badge-ok'>Connectat</span>"
            SENYAL="${SIGNAL_MAP[$mac]}"
        else
            ESTAT_BADGE="<span class='badge'>Desconnectat</span>"
            SENYAL="—"
        fi

        echo "<tr>"
        echo "  <td><code>$mac</code></td>"
        echo "  <td><code>$ip</code></td>"
        echo "  <td><strong style='color:#f8fafc'>$NOM_SHOW</strong></td>"
        echo "  <td>$SENYAL</td>"
        echo "  <td>$ESTAT_BADGE</td>"
        echo "</tr>"
    done < "$LEASES_FILE"
fi

if [ "$HAS_ROWS" -eq 0 ]; then
    echo "<tr><td colspan='5' class='text-dimmed text-small' style='text-align:center'>Cap client amb lease actiu</td></tr>"
fi

cat << EOM
            </tbody>
        </table>
    </div>

EOM

# --- Card info driver/interfície ---
DRIVER_ACTIU=$(lsmod | grep -E "^8821ce|^rtw88_8821ce" | awk '{print $1}' | head -1)
[ -z "$DRIVER_ACTIU" ] && DRIVER_ACTIU="desconegut"

IFACE_ACTUAL="$WIFI_IF"
IFACE_ESTAT=$(cat /sys/class/net/$WIFI_IF/operstate 2>/dev/null || echo "no disponible")

IP_ACTUAL=$(ip addr show "$WIFI_IF" 2>/dev/null | grep "inet " | awk '{print $2}' | head -1)
[ -z "$IP_ACTUAL" ] && IP_ACTUAL="sense IP"

cat << EOM
    <!-- Card info hardware -->
    <div class="card">
        <h2>🔧 Informació del driver WiFi</h2>
        <table>
            <tbody>
                <tr>
                    <td><strong>Interfície activa</strong></td>
                    <td><code>$IFACE_ACTUAL</code>
                        <span class="text-dimmed text-small">
                            (canviar a <em>wifi.conf</em> → camp WIFI_IF)
                        </span>
                    </td>
                </tr>
                <tr>
                    <td><strong>Estat interfície</strong></td>
                    <td><code>$IFACE_ESTAT</code> &nbsp; <code>$IP_ACTUAL</code></td>
                </tr>
                <tr>
                    <td><strong>Driver del kernel</strong></td>
                    <td><code>$DRIVER_ACTIU</code>
                        <span class="text-dimmed text-small">
                            (si no funciona l'AP, comprova que el driver correcte està carregat)
                        </span>
                    </td>
                </tr>
                <tr>
                    <td><strong>Blacklist rtw88</strong></td>
                    <td>
EOM

if [ -f /etc/modprobe.d/blacklist-rtw88.conf ]; then
    echo "<span class='badge badge-ok'>Activa</span> <span class='text-dimmed text-small'>/etc/modprobe.d/blacklist-rtw88.conf</span>"
else
    echo "<span class='badge badge-warn'>No configurada</span> <span class='text-dimmed text-small'>Si el driver rtw88 interfereix, cal crear-la</span>"
fi

cat << EOM
                    </td>
                </tr>
            </tbody>
        </table>
        <div class="alert-info mt-md text-small">
            💡 Si instal·les JSBach en un altre equip, el script detecta automàticament la interfície WiFi
            i actualitza <code>conf/wifi.conf</code>. Pots canviar-la manualment editant el camp <strong>WIFI_IF</strong>.
            Si el driver no suporta mode AP, instal·la el driver DKMS corresponent.
        </div>
    </div>

</div>
</body>
</html>
EOM
