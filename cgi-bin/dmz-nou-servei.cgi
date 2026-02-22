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
    <title>Obrir nou servei DMZ</title>
</head>
<body>
    <div class="container">
        <div class="card">
            <h2>🌐 Obrir nou servei</h2>
            <form action='/cgi-bin/dmz-agregar.cgi' method='get'>
                <div class="form-group">
                    <label>Port</label>
                    <input type='number' name='port' min='1' max='65535' placeholder='Ex: 80' required>
                </div>
                <div class="form-group">
                    <label>Protocol</label>
                    <select name='proto' required>
                        <option value='tcp'>TCP</option>
                        <option value='udp'>UDP</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>IP Servidor</label>
                    <input type='text' name='ipdmz' pattern='^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$' placeholder='Ex: 10.0.0.100' required title="Format d'IP vàlid">
                </div>
                <div class="btn-group">
                    <a href="/cgi-bin/dmz-configurar.cgi" class="btn btn-back">Enrere</a>
                    <button type='submit' class="btn btn-submit">Crear Servei</button>
                </div>
            </form>
        </div>
    </div>
</body>
</html>
EOM
