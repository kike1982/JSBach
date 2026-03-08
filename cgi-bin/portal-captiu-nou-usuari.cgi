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
    <title>Nou usuari - Portal Captiu</title>
</head>
<body>
<div class="container">
    <div class="card card-portal">
        <h2>Afegir nou usuari al portal captiu</h2>
        <form action="/cgi-bin/portal-captiu-afegir.cgi" method="get">
            <div class="form-group">
                <label>Nom d'usuari</label>
                <input type="text" name="usuari"
                    pattern="^[a-zA-Z0-9_-]+$"
                    placeholder="Ex: client1"
                    title="Nomes lletres, numeros, guio i guio baix"
                    maxlength="32"
                    required>
            </div>
            <div class="form-group">
                <label>Contrasenya</label>
                <input type="text" name="pass"
                    placeholder="Contrasenya d'acces"
                    maxlength="64"
                    required>
            </div>
            <div class="btn-group">
                <a href="/cgi-bin/portal-captiu-configurar.cgi" class="btn btn-ghost">Enrere</a>
                <button type="submit" class="btn btn-primary">Afegir usuari</button>
            </div>
        </form>
    </div>
</div>
</body>
</html>
EOM
