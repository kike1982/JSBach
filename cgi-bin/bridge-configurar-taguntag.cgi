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
    <meta charset="utf-8">
    <title>Configuració Tag-Untag</title>
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
        h2 {
            color: #3b82f6;
            margin-top: 20px;
            margin-bottom: 30px;
            font-size: 1.5rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border-left: 4px solid #3b82f6;
            padding-left: 15px;
        }
        .card {
            background: #1e293b;
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
        }
        th {
            text-align: left;
            color: #64748b;
            padding: 12px 14px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            font-size: 0.85rem;
            text-transform: uppercase;
        }
        td {
            padding: 16px 14px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            color: #f1f5f9;
        }
        .btn {
            padding: 8px 16px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.85rem;
            transition: all 0.2s;
            background: #3b82f6;
            color: white;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        .btn:hover {
            background: #2563eb;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }
        .iface-name { font-weight: 700; color: #3b82f6; font-family: monospace; }
        .vlan-badge { background: rgba(59, 130, 246, 0.1); color: #60a5fa; padding: 2px 8px; border-radius: 4px; font-family: monospace; }
    </style>
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
