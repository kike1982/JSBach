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

VLAN_DATA="$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge configurar mostrar bridge)"

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
    <link rel="stylesheet" href="/cgi-bin/style.cgi">
    <meta charset="utf-8">
    <title>Configuració Tag-Untag</title>
</head>
<body>
    <div class="container">
        <h2>🏷️ Configuració Tag-Untag</h2>
        <div class="card">
            <table>
                <tr><th>Interfaç</th><th>UNTAG</th><th>TAG</th><th>Accions</th></tr>
EOM

for iface in $(Interfaces_Ethernet); do
    linia_int=$(echo "$VLAN_DATA" | grep -E "^${iface};")
    VLAN_UNTAG=$(echo "$linia_int" | cut -d';' -f2)
    [[ -z "$VLAN_UNTAG" ]] && VLAN_UNTAG="0"
    VLAN_TAG_RAW=$(echo "$linia_int" | cut -d';' -f3)
    
    # Format VLAN ranges
    if [[ -n "$VLAN_TAG_RAW" && "$VLAN_TAG_RAW" != "0" ]]; then
        # Convert comma-separated to sorted array
        IFS=',' read -ra VIDS <<< "$VLAN_TAG_RAW"
        IFS=$'\n' sorted_vids=($(sort -n <<<"${VIDS[*]}"))
        unset IFS
        
        VLAN_TAG=""
        start=${sorted_vids[0]}
        prev=$start
        
        for ((i=1; i<=${#sorted_vids[@]}; i++)); do
            curr=${sorted_vids[i]}
            if [[ "$curr" != $((prev + 1)) ]]; then
                if [[ "$start" == "$prev" ]]; then
                    VLAN_TAG="${VLAN_TAG}${start},"
                else
                    VLAN_TAG="${VLAN_TAG}${start}-${prev},"
                fi
                start=$curr
            fi
            prev=$curr
        done
        VLAN_TAG="${VLAN_TAG%,}"
    else
        VLAN_TAG="0"
    fi
    
    echo "<tr>"
    echo "  <td><span class='iface-name'>$iface</span></td>"
    echo "  <td><span class='vlan-badge'>$VLAN_UNTAG</span></td>"
    echo "  <td><span class='vlan-badge'>$VLAN_TAG</span></td>"
    echo "  <td><a href='/cgi-bin/bridge-modificar-taguntag.cgi?int=$iface' class='btn'>✏️ Modificar</a></td>"
    echo "</tr>"
done

cat << EOM
            </table>
        </div>
    </div>
</body>
</html>
EOM
