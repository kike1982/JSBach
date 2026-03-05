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
<title>Afegir IP WLS</title>
</head>
<body>
<div class="container">
    <h2>Afegir IP amb Accés No Restringit</h2>
    <form action='/cgi-bin/tallafocs-ips-wls.cgi' method='get'>
        <input type='hidden' name='accio' value='afegir_ip_wls'>
        <div class="card">
            <div class="card-header"><h3 class="card-title">Identificació de l'Host</h3></div>
            <div class="form-group">
                <label>VLAN ID (VID):</label>
                <input type='text' name='vid' required pattern='^[0-9]+$' title='Només números' placeholder='Ex: 10'>
            </div>
            <div class="form-group">
                <label>Adreça IP:</label>
                <input type='text' name='ip' required pattern='^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}$' title='IP vàlida' placeholder='Ex: 192.168.10.50'>
            </div>
            <div class="form-group">
                <label>Adreça MAC:</label>
                <input type='text' name='mac' required pattern='^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$' title='MAC vàlida' placeholder='Ex: AA:BB:CC:DD:EE:FF'>
            </div>
        </div>

        <div class="btn-group">
            <a href="/cgi-bin/tallafocs-configuracio.cgi" class="btn btn-back">⬅Tornar</a>
            <button type="submit" class="btn btn-submit">Registrar IP</button>
        </div>
    </form>
</div>
</body>
</html>
EOM
