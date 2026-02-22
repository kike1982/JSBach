#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

/bin/cat <<'EOM'
<!DOCTYPE html>
<html lang="es">
<head>
    <link rel="stylesheet" href="/cgi-bin/style.cgi">
    <meta charset="utf-8">
    <title>Resultat Configuració WAN</title>
    <script>
        setTimeout(() => {
            window.location.href = '/cgi-bin/ifwan.cgi?comand=estat';
        }, 3000);
    </script>
</head>
<body>
    <div class="container">
        <h2>💾 Guardant Configuració</h2>
        <div style="text-align:center; margin-bottom:20px; color:#94a3b8;">
            Redirigint a l'estat en 3 segons...
        </div>
EOM

mode=$(echo "$QUERY_STRING" | sed -n 's/^.*mode=\([^&]*\).*$/\1/p')
int=$(echo "$QUERY_STRING" | sed -n 's/^.*int=\([^&]*\).*$/\1/p')
if [[ "$mode" == "manual" ]]; then
	ip=$(echo "$QUERY_STRING" | sed -n 's/^.*ip=\([^&]*\).*$/\1/p')
	masc=$(echo "$QUERY_STRING" | sed -n 's/^.*masc=\([^&]*\).*$/\1/p')
	pe=$(echo "$QUERY_STRING" | sed -n 's/^.*pe=\([^&]*\).*$/\1/p')
	dns=$(echo "$QUERY_STRING" | sed -n 's/^.*dns=\([^&]*\).*$/\1/p')
fi

if [[ ! -z $ip ]]; then
	ipmas="$ip/$masc"
fi

ordre="ifwan configurar $mode $int $ipmas $pe $dns"

# --- Caja con los valores recibidos ---
echo '<div class="card">'
echo '  <div class="card-header"><h3 class="card-title">🔍 Valors Aplicats</h3></div>'
echo '  <table class="info-table">'
echo "    <tr><th>Mode</th><td><span style='color:#3b82f6; text-transform:uppercase;'>$mode</span></td></tr>"
echo "    <tr><th>Interfície</th><td>$int</td></tr>"
if [[ "$mode" == "manual" ]]; then
    echo "    <tr><th>IP / Máscara</th><td>$ipmas</td></tr>"
    echo "    <tr><th>Porta d'enllaç</th><td>$pe</td></tr>"
    echo "    <tr><th>DNS</th><td>$dns</td></tr>"
fi
echo '  </table>'
echo '</div>'

# --- Caja con la salida del comando ---
echo '<div class="card">'
echo '  <div class="card-header"><h3 class="card-title">⚙️ Resultat del Sistema</h3></div>'
echo '  <div class="output-box">'
echo "$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli $ordre)"
echo '  </div>'
echo '</div>'

echo '    </div>'
echo '</body>'
echo '</html>'