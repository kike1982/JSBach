#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="utf-8">
    <title>Estat DMZ</title>
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
            max-width: 800px;
            margin: 0 auto;
        }
        .card {
            background: #1e293b;
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        }
        h2 {
            color: #3b82f6;
            margin-bottom: 20px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .output {
            background: #0f172a;
            border-left: 4px solid #3b82f6;
            padding: 16px;
            border-radius: 8px;
            margin-top: 10px;
        }
        pre {
            margin: 0;
            font-family: 'Fira Code', monospace;
            font-size: 0.9rem;
            color: #e2e8f0;
            white-space: pre-wrap;
            word-break: break-all;
        }
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            background: rgba(16, 185, 129, 0.1);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.2);
            border-radius: 8px;
            font-weight: 700;
            margin-top: 15px;
        }
    </style>
</head>
<body>
<div class="container">
EOM

comand=$(echo "$QUERY_STRING" | sed -n 's/^.*comand=\([^&]*\).*$/\1/p')

# Emojis según comanda
case "$comand" in
    iniciar) ICON="🚀";;
    aturar)  ICON="🛑";;
    estat)   ICON="📊";;
    *)       ICON="⚙️";;
esac

echo "<div class='card'>"
echo "  <h2>$ICON Comanda: $comand</h2>" 
echo "  <div class='output'>"
echo "    <pre>$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dmz "$comand")</pre>"
echo "  </div>"

# Si no es 'estat', mostrar también el estado actual
if [[ "$comand" != "estat" ]]; then
    estat_actual=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dmz estat)
    echo "  <div class='status-badge'><span>🔍</span> Estat actual DMZ: $estat_actual</div>"
fi
echo "</div>"

cat << EOM
</div>
</body>
</html>
EOM
