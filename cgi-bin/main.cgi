#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

/bin/cat << EOM

<html>
<head>

EOM
echo '<title>Administración de '$HOSTNAME'</title>'
/bin/cat << EOM

<meta http-equiv="Content-Type" content="text/html; charset=windows-1252">
<meta content="MSHTML 6.00.2900.3660" name="GENERATOR"> 

<style type="text/css">
<!--
/* --- Estilo general del body --- */
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
    color: #e9ab17;
    text-shadow: 1px 1px 3px #555;
    transition: color 0.3s ease;
}
.estado:hover {
    color: #ffcc33;
}

/* --- Cabeceras con estilo moderno --- */
.cabecera {
    font-family: Verdana, Arial, Helvetica, sans-serif;
    font-size: 16px;
    color: #ffffff;
    background: linear-gradient(135deg, #4caf50, #2e7d32);
    padding: 10px 15px;
    border-radius: 8px;
    border: 1px solid #1b5e20;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.2);
    transition: background 0.3s ease, transform 0.2s ease;
}
.cabecera:hover {
    background: linear-gradient(135deg, #66bb6a, #388e3c);
    transform: scale(1.02);
}

/* --- Estilos adicionales --- */
.Estilo1 {
    color: #d500f9;
    font-weight: bold;
    text-shadow: 1px 1px 2px #aaa;
}

.Estilo2 {
    color: #212121;
    font-family: Arial, Helvetica, sans-serif;
}

/* --- Mensaje fallback --- */
noframes body {
    background: #fff3e0;
    color: #bf360c;
    padding: 20px;
    border-radius: 8px;
    border: 1px solid #ffcc80;
    font-size: 14px;
}
-->
</style>
</head> 

<frameset rows="18%,82%" frameborder="1">
<frame src="/cgi-bin/index-admin.cgi" name="menu-general" noresize="noresize">
<frameset cols="20%,80%">
<frame src="/cgi-bin/cos-admin.cgi" name="menu" noresize="noresize">
<frame src="/cgi-bin/info.cgi" name="body" noresize="noresize">
</frameset>

<noframes>
<body>Tu browser no soporta frames!</body>
</noframes>

</html>

EOM