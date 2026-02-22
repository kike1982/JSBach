#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="UTF-8">
<style>
/* --- Estil Modern Dark --- */
body {
    margin: 0;
    padding: 24px;
    background: #0f172a;
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    color: #f8fafc;
}

.menu-title {
    font-size: 0.75rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #64748b;
    margin-bottom: 20px;
    padding-left: 12px;
}

.menu-list {
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

/* Colores laterales sutiles */
.item-start { border-left: 4px solid #10b981; }
.item-stop  { border-left: 4px solid #ef4444; }
.item-status { border-left: 4px solid #3b82f6; }
.item-config { border-left: 4px solid #8b5cf6; }
.item-input  { border-left: 4px solid #f59e0b; }

</style>
</head>
<body>
    <div class="menu-title">Tallafocs (Firewall)</div>
    <div class="menu-list">
        <a href="/cgi-bin/tallafocs.cgi?comand=iniciar" class="menu-item item-start" target="body">
            <span class="icon">🚀</span> Iniciar Servei
        </a>
        <a href="/cgi-bin/tallafocs.cgi?comand=aturar" class="menu-item item-stop" target="body">
            <span class="icon">🛑</span> Aturar Servei
        </a>
        <a href="/cgi-bin/tallafocs.cgi?comand=estat" class="menu-item item-status" target="body">
            <span class="icon">📊</span> Estat Global
        </a>
        <a href="/cgi-bin/tallafocs-configuracio.cgi" class="menu-item item-config" target="body">
            <span class="icon">🛠️</span> Configuració
        </a>
        <a href="/cgi-bin/tallafocs-input.cgi" class="menu-item item-input" target="body">
            <span class="icon">📥</span> Regles d'Entrada
        </a>
    </div>
</body>
</html>
EOM



