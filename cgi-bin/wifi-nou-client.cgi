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
    <title>Afegir client WiFi</title>
</head>
<body>
<div class="container">
    <div class="card">
        <h2>🖥️ Afegir nou client WiFi</h2>
        <form action="/cgi-bin/wifi-agregar.cgi" method="get">
            <div class="form-group">
                <label>Adreça MAC</label>
                <input type="text" name="mac"
                    pattern="^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$"
                    placeholder="Ex: AA:BB:CC:DD:EE:FF"
                    title="Format MAC vàlid: XX:XX:XX:XX:XX:XX"
                    required>
            </div>
            <div class="form-group">
                <label>IP fixa assignada</label>
                <input type="text" name="ip"
                    pattern="^([0-9]{1,3}\.){3}[0-9]{1,3}$"
                    placeholder="Ex: 192.168.100.10"
                    title="Format d'IP vàlid"
                    required>
            </div>
            <div class="form-group">
                <label>Nom del dispositiu</label>
                <input type="text" name="nom"
                    placeholder="Ex: Mobil-Kike"
                    maxlength="30"
                    required>
            </div>
            <div class="btn-group">
                <a href="/cgi-bin/wifi-configurar.cgi" class="btn btn-back">Enrere</a>
                <button type="submit" class="btn btn-submit">Afegir client</button>
            </div>
        </form>
    </div>
</div>
</body>
</html>
EOM
