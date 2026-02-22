#!/bin/bash

# switch.cgi - Gestión de Switches (Unificado)

source /usr/local/JSBach/conf/variables.conf

get_switches() {
    [ -f "/usr/local/JSBach/conf/$SWITCHES_CONF" ] && grep -v "^#" "/usr/local/JSBach/conf/$SWITCHES_CONF" | grep -v "^$" | while IFS=';' read -r name ip user pass proto _; do
        [ -n "$ip" ] && echo "$name;$ip;$user;$pass;$proto"
    done
}

get_blocked_macs() {
    [ -f "/usr/local/JSBach/conf/$MACS_SWITCHES_CONF" ] && grep -v "^#" "/usr/local/JSBach/conf/$MACS_SWITCHES_CONF" | grep -v "^$"
}

get_admin_macs() {
    [ -f "/usr/local/JSBach/conf/$MAC_ADMIN_CONF" ] && grep -v "^#" "/usr/local/JSBach/conf/$MAC_ADMIN_CONF" | grep -v "^$"
}

if [ "$REQUEST_METHOD" = "POST" ]; then
    read -n $CONTENT_LENGTH POST_DATA
    get_val() { echo "$POST_DATA" | grep -oP "(?<=&|^)$1=.*?(?=&|$)" | cut -d= -f2 | sed 's/+/ /g' | perl -pe 's/%([0-9a-f]{2})/chr(hex($1))/eig'; }
else
    get_val() { echo "$QUERY_STRING" | grep -oP "(?<=&|^)$1=.*?(?=&|$)" | cut -d= -f2 | sed 's/+/ /g' | perl -pe 's/%([0-9a-f]{2})/chr(hex($1))/eig'; }
fi

comand=$(get_val comand)

print_header() {
    echo "Content-type: text/html; charset=utf-8"
    echo ""
    cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
    <link rel="stylesheet" href="/cgi-bin/style.cgi">
    <meta charset="utf-8">
    <title>Gestió de Switches - JSBach</title>
</head>
<body><div class="container">
EOF
}

print_footer() { echo "</div></body></html>"; }

case $comand in
    estat)
        print_header
        echo "<h1>📊 Estat Switch</h1><div class='card'><table><thead><tr><th>Nom</th><th>IP</th><th>Estat</th></tr></thead><tbody>"
        while IFS=';' read -r name ip user pass proto; do
            [ -z "$ip" ] && continue
            ID=$(echo "$ip" | sed 's/\./-/g')
            echo "<tr><td>$name</td><td><code>$ip</code></td><td><span id='s-$ID' class='status-badge'>🔄...</span></td></tr>"
            JS="$JS '$ip',"
        done < <(get_switches)
        echo "</tbody></table></div><script>
        [$JS].forEach(ip => {
            const el = document.getElementById('s-' + ip.replace(/\./g, '-'));
            fetch('/cgi-bin/switch.cgi?comand=p&ip=' + ip).then(r=>r.text()).then(d=>{
                el.textContent = d.trim()==='UP' ? '✅ Activo' : '❌ No Encontrado';
                el.className = 'status-badge ' + (d.trim()==='UP' ? 'status-active' : 'status-down');
            });
        });</script>"
        print_footer ;;
    p)
        echo "Content-type: text/plain"
        echo ""
        ping -c 1 -w 1 "$(get_val ip)" >/dev/null 2>&1 && echo "UP" || echo "DOWN"
        exit 0 ;;
    mostrar)
        print_header
        echo "<h1>📋 Taula MAC</h1>"
        while IFS=';' read -r n i u p pr; do
            [ -z "$i" ] && continue
            ping -c 1 -W 0.5 "$i" >/dev/null 2>&1 && echo "<div class='card'><h2>$n ($i)</h2><pre>$(/usr/local/JSBach/scripts/client_srv_cli switch configurar mostrar_tabla_macs "$i" "$u" "$p" "$pr" | sed '1,/SWITCH:/d')</pre></div>"
        done < <(get_switches)
        print_footer ;;
    gestion_mac)
        print_header
        echo "<h1>🛡️ Gestión de MAC</h1><div class='card'><h2>Acciones Globales</h2><a href='/cgi-bin/switch.cgi?comand=apply' class='btn btn-success'>🔒 Aplicar Bloqueos</a> <a href='/cgi-bin/switch.cgi?comand=clear' class='btn btn-error'>🔓 Borrar Bloqueos</a></div>"
        echo "<div class='card'><h2>Añadir MAC</h2><p style='font-size:0.8rem;color:#94a3b8;'>Bloquear MAC en una VLAN específica.</p><form action='/cgi-bin/switch.cgi' method='POST'><input type='hidden' name='comand' value='add_m'><div style='display:flex;gap:1rem;'><input type='text' name='mac' placeholder='XX:XX:XX:XX:XX:XX' required style='flex:1;'><select name='vlan' required style='flex:0.5;'><option value=''>VLAN</option><option value='1'>VLAN 1</option><option value='2'>VLAN 2</option><option value='3'>VLAN 3</option><option value='4'>VLAN 4</option></select><button type='submit' class='btn btn-primary'>➕ Añadir</button></div></form></div>"
        echo "<div class='card'><h2>MACs Bloqueadas</h2><table><thead><tr><th>MAC</th><th>VLAN</th><th>Estat</th><th>Accions</th></tr></thead><tbody>"
        while read -r line; do
            [ -z "$line" ] && continue
            if echo "$line" | grep -q ";"; then
                mac=$(echo "$line" | cut -d';' -f1)
                vlan=$(echo "$line" | cut -d';' -f2)
            else
                mac="$line"
                vlan="N/A"
            fi
            if grep -qF "$line" "/usr/local/JSBach/conf/mac_switches_applied.conf" 2>/dev/null; then
                status="<span class='status-badge status-active'>🔒 Bloqueada</span>"
            else
                status="<span class='status-badge' style='background:rgba(239,68,68,0.1);color:#f87171;'>🔓 Pendent</span>"
            fi
            mac_encoded=$(echo "$line" | sed 's/:/%3A/g' | sed 's/;/%3B/g')
            echo "<tr><td><code>$mac</code></td><td><span class='status-badge' style='background:rgba(59,130,246,0.2);color:#60a5fa;'>VLAN $vlan</span></td><td>$status</td><td><a href='/cgi-bin/switch.cgi?comand=del_m&mac=$mac_encoded' class='btn btn-error' style='font-size:0.7rem;padding:0.3rem 0.6rem;'>🗑️</a></td></tr>"
        done < <(get_blocked_macs)
        echo "</tbody></table>"
        echo "</div><script>
        fetch('/cgi-bin/switch.cgi?comand=verify_status').then(r=>r.text()).then(d=>{
            const active = d.trim() === 'OK';
            if (!active) {
                document.querySelectorAll('.mac-status-badge').forEach(el => {
                    if (el.textContent.includes('Bloqueada')) {
                        el.textContent = '⚠️ Error Sinc.';
                        el.style.background = 'rgba(234, 179, 8, 0.2)';
                        el.style.color = '#eab308';
                    }
                });
            }
        });</script>"
        print_footer ;;
    gestion_admin)
        print_header
        echo "<h1>🛡️ Gestión de Admin (VLAN1)</h1><div class='card'><h2>Acciones Globales</h2><a href='/cgi-bin/switch.cgi?comand=apply_admin' class='btn btn-success'>🔒 Aplicar Permisos</a> <a href='/cgi-bin/switch.cgi?comand=clear_admin' class='btn btn-error'>🔓 Borrar Reglas</a></div>"
        echo "<div class='card'><h2>Permitir MAC</h2><p style='font-size:0.8rem;color:#94a3b8;'>Las MACs indicadas podrán acceder. El resto serán bloqueadas.</p><form action='/cgi-bin/switch.cgi' method='POST'><input type='hidden' name='comand' value='add_admin_m'><div style='display:flex;gap:1rem;'><input type='text' name='mac' placeholder='XX:XX:XX:XX:XX:XX' required style='flex:1;'><button type='submit' class='btn btn-primary'>➕ Añadir</button></div></form></div>"
        echo "<div class='card'><h2>MACs Permitidas</h2>"
        for m in $(get_admin_macs); do
            if grep -qix "^$m$" "/usr/local/JSBach/conf/mac_admin_applied.conf" 2>/dev/null; then
                status="<span class='status-badge status-active admin-mac-status-badge' data-mac='$m'>✅ Permitida</span>"
            else
                status="<span class='status-badge admin-mac-status-badge' data-mac='$m' style='background:rgba(239,68,68,0.1);color:#f87171;border:1px solid rgba(239,68,68,0.2)'>🔓 Pendiente</span>"
            fi
            echo "<div class='mac-item'><span><code>$m</code> $status</span><a href='/cgi-bin/switch.cgi?comand=del_admin_m&mac=$m' class='btn btn-error btn-small' style='padding:0.2rem 0.5rem;'>🗑️</a></div>"
        done
        echo "</div><script>
        fetch('/cgi-bin/switch.cgi?comand=verify_admin_status').then(r=>r.text()).then(d=>{
            const active = d.trim() === 'OK';
            if (!active) {
                document.querySelectorAll('.admin-mac-status-badge').forEach(el => {
                    if (el.textContent.includes('Permitida')) {
                        el.textContent = '⚠️ Error Sinc.';
                        el.style.background = 'rgba(234, 179, 8, 0.2)';
                        el.style.color = '#eab308';
                    }
                });
            }
        });</script>"
        print_footer ;;
    verify_status)
        echo "Content-type: text/plain"
        echo ""
        /usr/local/JSBach/scripts/client_srv_cli switch configurar comprobar_acls | grep -q "FAIL" && echo "FAIL" || echo "OK"
        exit 0 ;;
    verify_admin_status)
        echo "Content-type: text/plain"
        echo ""
        /usr/local/JSBach/scripts/client_srv_cli switch configurar comprobar_acls_admin | grep -q "FAIL" && echo "FAIL" || echo "OK"
        exit 0 ;;
    add_m)
        /usr/local/JSBach/scripts/client_srv_cli switch configurar afegir_mac "$(get_val mac)" "$(get_val vlan)" >/dev/null 2>&1
        echo "Status: 302 Found"
        echo "Location: /cgi-bin/switch.cgi?comand=gestion_mac"
        echo ""
        exit 0 ;;
    add_admin_m)
        /usr/local/JSBach/scripts/client_srv_cli switch configurar afegir_mac_admin "$(get_val mac)" >/dev/null 2>&1
        echo "Status: 302 Found"
        echo "Location: /cgi-bin/switch.cgi?comand=gestion_admin"
        echo ""
        exit 0 ;;
    del_m)
        /usr/local/JSBach/scripts/client_srv_cli switch configurar eliminar_mac "$(get_val mac)" >/dev/null 2>&1
        echo "Status: 302 Found"
        echo "Location: /cgi-bin/switch.cgi?comand=gestion_mac"
        echo ""
        exit 0 ;;
    del_admin_m)
        /usr/local/JSBach/scripts/client_srv_cli switch configurar eliminar_mac_admin "$(get_val mac)" >/dev/null 2>&1
        echo "Status: 302 Found"
        echo "Location: /cgi-bin/switch.cgi?comand=gestion_admin"
        echo ""
        exit 0 ;;
    apply)
        print_header
        echo "<h1>🔒 Aplicando Bloqueos...</h1><div class='card'><pre>$(/usr/local/JSBach/scripts/client_srv_cli switch configurar crear_acls)</pre></div><a href='/cgi-bin/switch.cgi?comand=gestion_mac' class='btn btn-primary'>Volver</a>"
        print_footer ;;
    apply_admin)
        print_header
        echo "<h1>🔒 Aplicando Reglas Admin...</h1><div class='card'><pre>$(/usr/local/JSBach/scripts/client_srv_cli switch configurar crear_acls_admin)</pre></div><a href='/cgi-bin/switch.cgi?comand=gestion_admin' class='btn btn-primary'>Volver</a>"
        print_footer ;;
    clear)
        print_header
        echo "<h1>🔓 Borrando Bloqueos...</h1><div class='card'><pre>$(/usr/local/JSBach/scripts/client_srv_cli switch configurar eliminar_acls)</pre></div><a href='/cgi-bin/switch.cgi?comand=gestion_mac' class='btn btn-primary'>Volver</a>"
        print_footer ;;
    clear_admin)
        print_header
        echo "<h1>🔓 Borrando Reglas Admin...</h1><div class='card'><pre>$(/usr/local/JSBach/scripts/client_srv_cli switch configurar eliminar_acls_admin)</pre></div><a href='/cgi-bin/switch.cgi?comand=gestion_admin' class='btn btn-primary'>Volver</a>"
        print_footer ;;
    configurar)
        print_header
        echo "<h1>⚙️ Configuració Switch</h1><div class='card'><h2>Añadir Switch</h2><form action='/cgi-bin/switch.cgi' method='POST'><input type='hidden' name='comand' value='save_s'><div class='form-grid'><input type='text' name='n' placeholder='Nombre' required><input type='text' name='i' placeholder='IP' required><input type='text' name='u' placeholder='Usuario' value='admin' required><input type='password' name='p' placeholder='Password' required><select name='pr'><option value='ssh'>SSH</option><option value='telnet'>Telnet</option></select></div><button type='submit' class='btn btn-success'>💾 Guardar</button></form></div>"
        echo "<div class='card'><h2>Configurados</h2><table><thead><tr><th>Nom</th><th>IP</th><th>Usuario</th><th>Protocolo</th><th>Accions</th></tr></thead><tbody>"
        while IFS=';' read -r n i u p pr; do
            [ -z "$i" ] && continue
            echo "<tr><td>$n</td><td><code>$i</code></td><td>$u</td><td>${pr^^}</td><td><a href='/cgi-bin/switch.cgi?comand=del_s&ip=$i' class='btn btn-error btn-small' onclick='return confirm(\"¿Seguro?\")'>🗑️</a></td></tr>"
        done < <(get_switches)
        echo "</tbody></table></div>"
        print_footer ;;
    save_s)
        /usr/local/JSBach/scripts/client_srv_cli switch configurar afegir_switch "$(get_val n)" "$(get_val i)" "$(get_val u)" "$(get_val p)" "$(get_val pr)" >/dev/null 2>&1
        echo "Status: 302 Found"
        echo "Location: /cgi-bin/switch.cgi?comand=configurar"
        echo ""
        exit 0 ;;
    del_s)
        /usr/local/JSBach/scripts/client_srv_cli switch configurar eliminar_switch "$(get_val ip)" >/dev/null 2>&1
        echo "Status: 302 Found"
        echo "Location: /cgi-bin/switch.cgi?comand=configurar"
        echo ""
        exit 0 ;;
    *)
        print_header
        echo "<h1>Switches</h1><p>Seleccione una opción.</p>"
        print_footer ;;
esac

