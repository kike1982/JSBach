#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-Type:text/html;charset=utf-8"
/bin/cat << EOM

<html>
<head>
    <link rel="stylesheet" href="/cgi-bin/style.cgi">
<title>Administrant el Router</title>
<meta http-equiv="Content-Type" content="text/html; charset=windows-1252">
<meta content="MSHTML 6.00.2900.3660" name="GENERATOR">
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
      <button id="btn-home" onclick="home()" class="btn-active">INICIO</button>
      <button id="btn-wan" onclick="wan()">WAN</button>
      <button id="btn-enrutar" onclick="enrutar()">ENRUTAR</button>
      <button id="btn-bridge" onclick="bridge()">BRIDGE</button>
      <button id="btn-tallafocs" onclick="tallafocs()">TALLAFOCS</button>
      <button id="btn-dmz" onclick="dmz()">DMZ</button>
      <button id="btn-switch" onclick="switches()">SWITCH</button>
    </td>    
  </tr>
</table>

</body>
</html>

EOM