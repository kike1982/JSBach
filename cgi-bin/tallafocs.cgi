#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="utf-8">
<title>Gestió Tallafocs</title>
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
    margin-top: 0;
    margin-bottom: 24px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.card {
    background: #1e293b;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
}
.output {
    background: #0f172a;
    border-left: 4px solid #3b82f6;
    padding: 16px;
    border-radius: 8px;
    margin-top: 20px;
}
pre {
    margin: 0;
    font-family: 'Fira Code', monospace;
    font-size: 0.9rem;
    color: #e2e8f0;
    white-space: pre-wrap;
    word-break: break-all;
}
.simple-output {
    background: rgba(16, 185, 129, 0.1);
    border-left: 4px solid #10b981;
    color: #34d399;
    padding: 12px 16px;
    border-radius: 6px;
    font-weight: 600;
}
</style>
</head>
<body>
<div class="container">
EOM

comand=$(echo "$QUERY_STRING" | sed -n 's/^.*comand=\([^&]*\).*$/\1/p')

# Asignar Emoji según comando
ICON="⚙️"
[[ "$comand" == "iniciar" ]] && ICON="🚀"
[[ "$comand" == "aturar" ]] && ICON="🛑"
[[ "$comand" == "estat" ]] && ICON="📊"

echo "<h2>$ICON Acció: $comand</h2>"
echo "<div class='card'>"

if [[ "$comand" != "estat" ]]; then
	echo "<div class=\"simple-output\">$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs $comand)</div>"
else
	echo "<div class=\"output\"><pre>$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs $comand)</pre></div>"
fi

cat << EOM
</div>
</div>
</body>
</html>
EOM
