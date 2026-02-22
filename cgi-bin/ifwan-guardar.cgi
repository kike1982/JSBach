#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

/bin/cat <<'EOM'
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Resultat Configuració WAN</title>
    <style>
        body {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background: #0f172a;
            margin: 24px;
            color: #f8fafc;
            line-height: 1.5;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        h2 {
            text-align: center;
            color: #3b82f6;
            margin-bottom: 30px;
            font-weight: 800;
        }
        .card {
            background: #1e293b;
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        }
        .card-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 16px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            padding-bottom: 12px;
        }
        .card-title {
            font-size: 1.1rem;
            font-weight: 700;
            color: #94a3b8;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .info-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.95rem;
        }
        .info-table th {
            text-align: left;
            color: #64748b;
            padding: 12px 8px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            width: 40%;
        }
        .info-table td {
            padding: 12px 8px;
            color: #f1f5f9;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            font-weight: 500;
        }
        .output-box {
            background: #0f172a;
            border-radius: 8px;
            padding: 16px;
            font-family: 'Fira Code', monospace;
            font-size: 0.9rem;
            color: #e2e8f0;
            white-space: pre-wrap;
            border-left: 4px solid #3b82f6;
        }
    </style>
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