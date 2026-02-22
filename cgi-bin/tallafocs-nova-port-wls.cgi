#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="UTF-8">
<title>Afegir Port WLS</title>
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
    max-width: 600px;
    margin: 0 auto;
}
h2 {
    text-align: center;
    color: #10b981;
    margin-bottom: 30px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.05em;
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
    gap: 10px;
    margin-bottom: 20px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    padding-bottom: 12px;
}
.card-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #94a3b8;
    margin: 0;
}
.form-group {
    margin-bottom: 20px;
}
label {
    display: block;
    margin-bottom: 8px;
    font-weight: 600;
    color: #cbd5e1;
    font-size: 0.9rem;
}
input[type="text"], select {
    width: 100%;
    padding: 12px;
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 8px;
    color: #f8fafc;
    font-family: 'Fira Code', monospace;
    transition: all 0.2s;
    box-sizing: border-box;
    appearance: none;
}
input[type="text"]:focus, select:focus {
    outline: none;
    border-color: #10b981;
    box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2);
}
.btn-group {
    display: flex;
    gap: 15px;
    margin-top: 32px;
}
.btn {
    flex: 1;
    padding: 14px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 700;
    font-size: 1rem;
    transition: all 0.2s;
    text-transform: uppercase;
    letter-spacing: 0.025em;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
    text-decoration: none;
}
.btn-submit { background: #10b981; color: white; }
.btn-submit:hover { background: #059669; transform: translateY(-1px); }
.btn-back { background: #475569; color: white; }
.btn-back:hover { background: #334155; transform: translateY(-1px); }
</style>
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
