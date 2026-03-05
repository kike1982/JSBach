#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

/bin/cat << EOM

<html>
<head>
    <link rel="stylesheet" href="/cgi-bin/style.cgi">

EOM
echo '<title>Administración de '$HOSTNAME'</title>'
/bin/cat << EOM

<meta http-equiv="Content-Type" content="text/html; charset=windows-1252">
<meta content="MSHTML 6.00.2900.3660" name="GENERATOR">
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