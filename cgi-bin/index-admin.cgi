#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-Type:text/html;charset=utf-8"
/bin/cat << EOM

<html>
<head>
<title>Administrant el Router</title>
<meta http-equiv="Content-Type" content="text/html; charset=windows-1252">
<meta content="MSHTML 6.00.2900.3660" name="GENERATOR">

<style type="text/css">
<!--
/* --- Estilo general --- */
body {
    font-family: Verdana, Arial, Helvetica, sans-serif;
    background: #0f172a;
    margin: 0;
    padding: 10px;
    color: #f8fafc;
}

/* --- Estados destacados --- */
.estado {
    font-size: 18px;
    font-weight: bold;
    font-family: Georgia, "Times New Roman", Times, serif;
    color: #fbbf24;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
    transition: color 0.3s ease;
}
.estado:hover {
    color: #fcd34d;
}

/* --- Cabeceras --- */
.cabecera {
    font-family: Verdana, Arial, Helvetica, sans-serif;
    font-size: 16px;
    color: #ffffff;
    background: linear-gradient(135deg, #166534, #14532d);
    padding: 10px 15px;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 2px 2px 6px rgba(0,0,0,0.4);
    transition: background 0.3s ease, transform 0.2s ease;
}
.cabecera:hover {
    background: linear-gradient(135deg, #15803d, #166534);
    transform: scale(1.02);
}

/* --- Tablas --- */
th {
    text-align: left;
    background-color: #1e293b;
    padding: 8px;
    border-bottom: 2px solid #059669;
    color: #f8fafc;
}
td {
    padding: 6px 8px;
    color: #cbd5e1;
}

/* --- Botones --- */
button {
    background: #1e293b;
    color: #f8fafc;
    font-weight: 600;
    border: 1px solid rgba(255,255,255,0.1);
    padding: 10px 20px;
    margin: 5px;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
    text-transform: uppercase;
    letter-spacing: 0.025em;
    font-size: 0.8rem;
    box-shadow: 0 1px 2px rgba(0,0,0,0.3);
}

button:hover {
    background: #3b82f6;
    color: white;
    transform: translateY(-1px);
    box-shadow: 0 4px 6px rgba(0,0,0,0.4);
    border-color: #3b82f6;
}

button:active {
    transform: translateY(0);
}

/* Botón activo (azul) */
button.btn-active {
    background: #3b82f6;
    border-color: #2563eb;
}

button.btn-active:hover {
    background: #2563eb;
}

/* --- Estilos adicionales --- */
.Estilo1 {
    color: #e879f9;
    font-weight: bold;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
}
.Estilo2 {
    color: #f1f5f9;
    font-family: Arial, Helvetica, sans-serif;
}
-->
</style>
</head>
<body link="#fbbf24" vlink="#fbbf24" alink="#fbbf24">

EOM

echo "<h1 align=\"center\">Administrant el Router "$HOSTNAME" amb "$PROJECTE"</h1>"

/bin/cat << EOM

<script>
function setActive(id) {
    // Quitar la clase active de todos los botones
    const buttons = document.querySelectorAll('button');
    buttons.forEach(btn => btn.classList.remove('btn-active'));
    
    // Añadir la clase active al botón clicado
    const activeBtn = document.getElementById(id);
    if (activeBtn) {
        activeBtn.classList.add('btn-active');
    }
}

function home(){
    setActive('btn-home');
    window.top.frames['menu'].location.href='/cgi-bin/cos-admin.cgi';
    window.top.frames['body'].location.href='/cgi-bin/info.cgi';
}
function wan(){
    setActive('btn-wan');
    window.top.frames['menu'].location.href='/cgi-bin/ifwan-menu.cgi';
    window.top.frames['body'].location.href='/cgi-bin/ifwan.cgi?comand=estat&';
}
function enrutar(){
    setActive('btn-enrutar');
    window.top.frames['menu'].location.href='/cgi-bin/enrutar-menu.cgi';
    window.top.frames['body'].location.href='/cgi-bin/enrutar.cgi?comand=estat&';
}
function bridge(){
    setActive('btn-bridge');
    window.top.frames['menu'].location.href='/cgi-bin/bridge-menu.cgi';
    window.top.frames['body'].location.href='/cgi-bin/bridge.cgi?comand=estat&';
}
function tallafocs(){
    setActive('btn-tallafocs');
    window.top.frames['menu'].location.href='/cgi-bin/tallafocs-menu.cgi';
    window.top.frames['body'].location.href='/cgi-bin/tallafocs.cgi?comand=estat&';
}
function dmz(){
    setActive('btn-dmz');
    window.top.frames['menu'].location.href='/cgi-bin/dmz-menu.cgi';
    window.top.frames['body'].location.href='/cgi-bin/dmz.cgi?comand=estat&';
}
function switches(){
    setActive('btn-switch');
    window.top.frames['menu'].location.href='/cgi-bin/switch-menu.cgi';
    window.top.frames['body'].location.href='/cgi-bin/switch.cgi?comand=estat&';
}
</script>

<table width="100%">
  <tr>
    <td align="center">
      <!-- Botones de navegación -->
      <button id="btn-home" onclick="home()" class="btn-active">🏠 INICIO</button>
      <button id="btn-wan" onclick="wan()">🌐 WAN</button>
      <button id="btn-enrutar" onclick="enrutar()">⚡ ENRUTAR</button>
      <button id="btn-bridge" onclick="bridge()">🌉 BRIDGE</button>
      <button id="btn-tallafocs" onclick="tallafocs()">🔥 TALLAFOCS</button>
      <button id="btn-dmz" onclick="dmz()">🛡️ DMZ</button>
      <button id="btn-switch" onclick="switches()">🔌 SWITCH</button>
    </td>    
  </tr>
</table>

</body>
</html>

EOM