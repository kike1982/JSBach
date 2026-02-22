#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
    <link rel="stylesheet" href="/cgi-bin/style.cgi">
<meta charset="UTF-8">
<title>Afegir Port WLS</title>
</head>
<body>
<div class="container">
    <h2>➕ Afegir Port WLS</h2>
    <form action='/cgi-bin/tallafocs-ports-wls.cgi' method='get'>
        <input type='hidden' name='accio' value='afegir_port_wls'>
        <div class="card">
            <div class="card-header"><h3 class="card-title">⚙️ Paràmetres del Port</h3></div>
            <div class="form-group">
                <label>Protocol:</label>
                <select name='protocol' required>
                    <option value='tcp'>TCP</option>
                    <option value='udp'>UDP</option>
                </select>
            </div>
            <div class="form-group">
                <label>Número de Port:</label>
                <input type='text' name='port' required pattern='^[0-9]+$' title='Només números' placeholder='Ex: 80'>
            </div>
        </div>

        <div class="btn-group">
            <a href="/cgi-bin/tallafocs-configuracio.cgi" class="btn btn-back">⬅️ Tornar</a>
            <button type="submit" class="btn btn-submit">🚀 Afegir Port</button>
        </div>
    </form>
</div>
</body>
</html>
EOM
