#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

/bin/cat << EOM

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <style type="text/css">
    /* --- Estilos Modernos Dark --- */
    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        background-color: #0f172a;
        margin: 0;
        padding: 24px;
        color: #f8fafc;
    }

    h4 {
        margin: 12px 0;
    }

    /* Enlaces como botones modernos */
    h4 a {
        display: block;
        padding: 14px 18px;
        text-decoration: none;
        font-weight: 600;
        color: #f1f5f9;
        background: #1e293b;
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        display: flex;
        align-items: center;
        gap: 12px;
    }

    h4 a:hover {
        background: #3b82f6;
        color: #ffffff;
        transform: translateX(4px);
        border-color: #60a5fa;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    }
    </style>
</head>
<body>
    <h4><a href="/cgi-bin/bridge.cgi?comand=iniciar&" target="body">🚀 Iniciar Bridge</a></h4>
    <h4><a href="/cgi-bin/bridge.cgi?comand=aturar&" target="body">🛑 Aturar Bridge</a></h4>
    <h4><a href="/cgi-bin/bridge.cgi?comand=estat&" target="body">📊 Estat Actual</a></h4>
    <h4><a href="/cgi-bin/bridge-configurar-taguntag.cgi" target="body">🏷️ Tag / Untag</a></h4>
    <h4><a href="/cgi-bin/bridge-configurar-ebtables.cgi" target="body">🛡️ Aïllament (ebtables)</a></h4>
    <h4><a href="/cgi-bin/bridge-configurar.cgi" target="body">⚙️ Gestió VLANs</a></h4>
</body>
</html>
EOM