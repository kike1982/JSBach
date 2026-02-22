#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="utf-8">
    <style>
        /* --- Estil Modern Dark --- */
        body {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background: #0f172a;
            color: #f8fafc;
            margin: 0;
            padding: 16px;
            overflow-x: hidden;
        }
        .menu-container {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .menu-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 16px;
            text-decoration: none;
            color: #94a3b8;
            background: #1e293b;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid rgba(255,255,255,0.05);
        }
        .menu-item:hover {
            background: #334155;
            color: #f8fafc;
            transform: translateX(4px);
            border-color: rgba(255,255,255,0.1);
        }
        .menu-item.active {
            background: #3b82f6;
            color: white;
        }
        .icon {
            font-size: 1.25rem;
            width: 24px;
            display: flex;
            justify-content: center;
        }
        .label {
            white-space: nowrap;
        }
    </style>
</head>
<body>
<div class="menu-container">
    <a href="/cgi-bin/dmz.cgi?comand=iniciar" target="body" class="menu-item"><span class="icon">🚀</span><span class="label">DMZ Iniciar</span></a>
    <a href="/cgi-bin/dmz.cgi?comand=aturar" target="body" class="menu-item"><span class="icon">🛑</span><span class="label">DMZ Aturar</span></a>
    <a href="/cgi-bin/dmz.cgi?comand=estat" target="body" class="menu-item"><span class="icon">📊</span><span class="label">DMZ Estat</span></a>
    <a href="/cgi-bin/dmz-configurar.cgi" target="body" class="menu-item"><span class="icon">🛠️</span><span class="label">DMZ Configuració</span></a>
</div>
</body>
</html>
EOM
