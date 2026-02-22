#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

urldecode() {
    local data="${1//+/ }"
    printf '%b' "${data//%/\\x}"
}

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="utf-8">
    <title>Resultat Operació IP WLS</title>
    <style>
        /* --- Estil Modern Dark --- */
        body {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background: #0f172a;
            color: #f8fafc;
            margin: 0;
            padding: 24px;
            line-height: 1.6;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }
        .container {
            max-width: 800px;
            width: 100%;
        }
        h2 {
            text-align: center;
            color: #f8fafc;
            margin-bottom: 30px;
            font-weight: 800;
        }
        .card {
            background: #1e293b;
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 32px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
            text-align: center;
        }
        .output-box {
            background: #0f172a;
            border-radius: 8px;
            padding: 20px;
            font-family: 'Fira Code', monospace;
            font-size: 0.9rem;
            color: #e2e8f0;
            white-space: pre-wrap;
            border-left: 4px solid #10b981;
            text-align: left;
            margin-top: 20px;
        }
        .redirect-text {
            margin-top: 20px;
            color: #94a3b8;
            font-size: 0.85rem;
        }
        .icon {
            font-size: 4rem;
            margin-bottom: 20px;
            display: block;
        }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-top: 20px;
            text-align: left;
            font-size: 0.9rem;
        }
        .info-item {
            background: rgba(255,255,255,0.05);
            padding: 10px;
            border-radius: 6px;
        }
        .info-label { color: #64748b; font-weight: 600; display: block; margin-bottom: 4px; }
        .info-value { color: #10b981; font-weight: 700; }
    </style>
    <script>
        setTimeout(() => {
            window.location.href = '/cgi-bin/tallafocs-configuracio.cgi';
        }, 3000);
    </script>
</head>
<body>
    <div class="container">
EOM

accio=$(echo "$QUERY_STRING" | sed -n 's/^.*accio=\([^&]*\).*$/\1/p')
vid=$(echo "$QUERY_STRING" | sed -n 's/^.*vid=\([^&]*\).*$/\1/p')
ip=$(echo "$QUERY_STRING" | sed -n 's/^.*ip=\([^&]*\).*$/\1/p')
mac=$(echo "$QUERY_STRING" | sed -n 's/^.*mac=\([^&]*\).*$/\1/p')

accio=$(urldecode "$accio")
vid=$(urldecode "$vid")
ip=$(urldecode "$ip")
mac=$(urldecode "$mac")

echo "      <div class='card'>"
echo "          <span class='icon'>🖥️</span>"
echo "          <h2>Whitelist d'IPs</h2>"
echo "          <div class='info-grid'>"
echo "              <div class='info-item'><span class='info-label'>Acció</span><span class='info-value'>$accio</span></div>"
echo "              <div class='info-item'><span class='info-label'>VID</span><span class='info-value'>$vid</span></div>"
echo "              <div class='info-item'><span class='info-label'>IP</span><span class='info-value'>$ip</span></div>"
echo "              <div class='info-item'><span class='info-label'>MAC</span><span class='info-value'>$mac</span></div>"
echo "          </div>"
echo "          <div class='output-box'><pre>$("$DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli" tallafocs configurar "$accio" "$vid" "$ip" "$mac")</pre></div>"
echo "          <div class='redirect-text'>Redirigint a la configuració en 3 segons...</div>"
echo "      </div>"

cat << EOM
    </div>
</body>
</html>
EOM
