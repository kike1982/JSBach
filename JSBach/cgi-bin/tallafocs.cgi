#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
    <link rel="stylesheet" href="/cgi-bin/style.cgi">
<meta charset="utf-8">
<title>Gestió Tallafocs</title>
</head>
<body>
<div class="container">
EOM

comand=$(echo "$QUERY_STRING" | sed -n 's/^.*comand=\([^&]*\).*$/\1/p')

# Asignar Emoji según comando
ICON=""
[[ "$comand" == "iniciar" ]] && ICON=""
[[ "$comand" == "aturar" ]] && ICON=""
[[ "$comand" == "estat" ]] && ICON=""

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
