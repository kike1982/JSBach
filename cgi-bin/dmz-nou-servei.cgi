#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="utf-8">
    <title>Obrir nou servei DMZ</title>
    <style>
        /* --- Estil Modern Dark --- */
        body {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background: #0f172a;
            color: #f8fafc;
            margin: 0;
            padding: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }
        .container {
            max-width: 600px;
            width: 100%;
        }
        .card {
            background: #1e293b;
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 32px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        }
        h2 {
            color: #f8fafc;
            margin-bottom: 32px;
            font-weight: 800;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .form-group {
            margin-bottom: 24px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #94a3b8;
            font-weight: 600;
            font-size: 0.9rem;
            text-transform: uppercase;
        }
        input[type="text"], input[type="number"], select {
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
        input:focus, select:focus {
            outline: none;
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
        }
        .btn-group {
            display: flex;
            gap: 15px;
            margin-top: 32px;
        }
        .btn {
            flex: 1;
            padding: 12px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 700;
            text-transform: uppercase;
            transition: all 0.2s;
            text-decoration: none;
            text-align: center;
            display: inline-block;
        }
        .btn-submit { background: #3b82f6; color: white; }
        .btn-submit:hover { background: #2563eb; transform: translateY(-1px); }
        .btn-back { background: #475569; color: white; }
        .btn-back:hover { background: #334155; transform: translateY(-1px); }
    </style>
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
