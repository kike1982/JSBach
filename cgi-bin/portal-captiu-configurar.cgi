#!/bin/bash

source /usr/local/JSBach/conf/variables.conf
source "$DIR/$PROJECTE/$DIR_CONF/$PORTAL_CAPTIU_SETTINGS_CONF"

echo "Content-type: text/html; charset=utf-8"
echo ""

NOW=$(date +%s)

# Obtenir llista d'usuaris
USUARIS_HTML=""
while IFS= read -r line; do
    [[ -z "$line" || "$line" =~ ^# ]] && continue

    USER=$(echo "$line" | cut -d';' -f1 | xargs)
    IP=$(echo "$line" | cut -d';' -f2 | xargs)
    TIMESTAMP=$(echo "$line" | cut -d';' -f3 | xargs)
    ESTAT=$(echo "$line" | cut -d';' -f4 | xargs)

    if [[ "$ESTAT" == "CONNECTAT" && -n "$IP" ]]; then
        BADGE="<span class='badge badge-ok'>CONNECTAT</span>"
        IP_SHOW="<code>$IP</code>"
        if [[ -n "$TIMESTAMP" && "$TIMESTAMP" =~ ^[0-9]+$ && "$TIMESTAMP" != "0" ]]; then
            INICI=$(date -d "@$TIMESTAMP" "+%H:%M %d/%m/%Y" 2>/dev/null || echo "$TIMESTAMP")
        else
            INICI="—"
        fi
    else
        BADGE="<span class='badge badge-muted'>DESCONNECTAT</span>"
        IP_SHOW="<span class='text-dimmed'>—</span>"
        INICI="—"
    fi

    USUARIS_HTML+="<tr>"
    USUARIS_HTML+="<td><strong style='color:#f8fafc'>$USER</strong></td>"
    USUARIS_HTML+="<td>$IP_SHOW</td>"
    USUARIS_HTML+="<td class='text-small text-dimmed'>$INICI</td>"
    USUARIS_HTML+="<td>$BADGE</td>"
    USUARIS_HTML+="<td class='text-right'><a href='/cgi-bin/portal-captiu-eliminar.cgi?usuari=$USER' class='btn btn-danger btn-sm'>Eliminar</a></td>"
    USUARIS_HTML+="</tr>"

done < <("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli portal-captiu configurar llistar_usuaris)

if [[ -z "$USUARIS_HTML" ]]; then
    USUARIS_HTML="<tr><td colspan='5' class='text-dimmed text-small' style='text-align:center'>Cap usuari configurat</td></tr>"
fi

# Durada sessio en format llegible
DUR_H=$((SESSION_DURATION / 60))
DUR_M=$((SESSION_DURATION % 60))
if [[ "$DUR_H" -gt 0 ]]; then
    DUR_LABEL="${DUR_H}h ${DUR_M}min"
else
    DUR_LABEL="${DUR_M}min"
fi

# Badge cron
if [[ "$CRON_ENABLED" == "1" ]]; then
    CRON_BADGE="<span class='badge badge-ok'>ACTIU</span>"
    CRON_DESC="Comprovant sessions cada <strong>${CRON_INTERVAL} minuts</strong>"
    CRON_BTN_TOGGLE="<a href='/cgi-bin/portal-captiu-guardar-cron.cgi?accio=desactivar' class='btn btn-danger'>Desactivar cron</a>"
else
    CRON_BADGE="<span class='badge badge-muted'>INACTIU</span>"
    CRON_DESC="El cron no esta configurat. Activa'l per netejar sessions automaticament."
    CRON_BTN_TOGGLE="<a href='/cgi-bin/portal-captiu-guardar-cron.cgi?accio=activar' class='btn btn-success'>Activar cron</a>"
fi

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
    <link rel="stylesheet" href="/cgi-bin/style.cgi">
    <meta charset="utf-8">
    <title>Portal Captiu - Configuracio</title>
</head>
<body>
<div class="container">

    <!-- Llista d'usuaris -->
    <div class="card card-portal">
        <div class="header-actions">
            <h2>Usuaris del portal captiu</h2>
            <a href="/cgi-bin/portal-captiu-nou-usuari.cgi" class="btn btn-success">Afegir usuari</a>
        </div>
        <table>
            <thead>
                <tr>
                    <th>Usuari</th>
                    <th>IP activa</th>
                    <th>Inici sessio</th>
                    <th>Estat</th>
                    <th class="text-right">Accions</th>
                </tr>
            </thead>
            <tbody>
                $USUARIS_HTML
            </tbody>
        </table>
    </div>

    <!-- Configuracio durada sessio i cron -->
    <div class="card">
        <h2>Configuracio de sessions</h2>
        <form action="/cgi-bin/portal-captiu-guardar-config.cgi" method="get">
            <div class="grid grid-2">
                <div class="form-group">
                    <label>Durada de la sessio (minuts)</label>
                    <input type="number" name="durada" value="$SESSION_DURATION" min="1" max="9999" required>
                    <p class="text-small text-dimmed mt-xs">Actual: ${SESSION_DURATION} min (${DUR_LABEL})</p>
                </div>
                <div class="form-group">
                    <label>Interval de verificacio cron (minuts)</label>
                    <input type="number" name="interval" value="$CRON_INTERVAL" min="1" max="60" required>
                    <p class="text-small text-dimmed mt-xs">Frequencia amb que el cron comprova sessions expirades</p>
                </div>
            </div>
            <div class="btn-group">
                <button type="submit" class="btn btn-primary">Guardar configuracio</button>
            </div>
        </form>
    </div>

    <!-- Control del cron -->
    <div class="card">
        <div class="header-actions">
            <div>
                <h2>Verificacio automatica (cron)</h2>
                <p class="text-small text-dimmed mt-xs">$CRON_DESC</p>
            </div>
            $CRON_BADGE
        </div>
        <div class="btn-group mt-md">
            $CRON_BTN_TOGGLE
            <a href="/cgi-bin/portal-captiu-guardar-cron.cgi?accio=netejar" class="btn btn-warn">Netejar sessions ara</a>
        </div>
    </div>

</div>
</body>
</html>
EOM
