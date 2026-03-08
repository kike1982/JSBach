#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

USER=$(echo "$QUERY_STRING" | sed -n 's/^.*user=\([^&]*\).*$/\1/p' | sed 's/+/ /g; s/%20/ /g')
PASS=$(echo "$QUERY_STRING" | sed -n 's/^.*pass=\([^&]*\).*$/\1/p' | sed 's/+/ /g; s/%20/ /g')

# Obtenir IP del client (la que Apache veu com a origen)
CLIENT_IP="$REMOTE_ADDR"

# Obtenir MAC del client des de la taula ARP
CLIENT_MAC=$(arp -n 2>/dev/null | grep "^$CLIENT_IP " | awk '{print $3}')

if [[ -z "$CLIENT_IP" ]]; then
    cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="3;url=/cgi-bin/portal-captiu-login.cgi?msg=No+s%27ha+pogut+obtenir+la+IP">
    <title>Error</title>
</head>
<body>
<p>No s'ha pogut obtenir la IP del client. Tornant...</p>
</body>
</html>
EOM
    exit 0
fi

if [[ -z "$CLIENT_MAC" || "$CLIENT_MAC" == "(incomplete)" ]]; then
    # Intentar ping per poblar ARP i tornar a provar
    ping -c 1 -W 1 "$CLIENT_IP" >/dev/null 2>&1
    CLIENT_MAC=$(arp -n 2>/dev/null | grep "^$CLIENT_IP " | awk '{print $3}')
fi

if [[ -z "$CLIENT_MAC" || "$CLIENT_MAC" == "(incomplete)" ]]; then
    CLIENT_MAC="00:00:00:00:00:00"
fi

# Cridar backend per autenticar
RESULTAT=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli portal-captiu autenticar "$USER" "$PASS" "$CLIENT_IP" "$CLIENT_MAC")

if echo "$RESULTAT" | grep -q "^OK"; then
    # Autenticacio correcta - mostrar pagina d'exit
    cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Connectat - Portal WiFi</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        :root { --bg-base:#0d1117; --bg-surface:#161b22; --ok:#3fb950; --t1:#e6edf3; --t2:#8b949e; --bd:rgba(255,255,255,0.08); }
        *, *::before, *::after { box-sizing:border-box; margin:0; padding:0; }
        body { font-family:'Inter',system-ui,sans-serif; background:var(--bg-base); color:var(--t1); min-height:100vh; display:flex; align-items:center; justify-content:center; padding:1.5rem; }
        .card { background:var(--bg-surface); border:1px solid var(--bd); border-left:3px solid var(--ok); border-radius:12px; padding:2.5rem; text-align:center; max-width:400px; width:100%; box-shadow:0 8px 24px rgba(0,0,0,0.6); }
        .icon { font-size:3rem; margin-bottom:1rem; }
        h1 { font-size:1.5rem; font-weight:700; margin-bottom:0.5rem; color:var(--t1); }
        p { color:var(--t2); font-size:0.9rem; margin-bottom:1rem; }
        .info { font-size:0.8rem; color:var(--t2); margin-top:1rem; }
        .btn { display:inline-block; padding:0.65rem 1.5rem; background:#3fb950; color:white; border-radius:8px; font-weight:700; font-family:inherit; font-size:0.95rem; text-decoration:none; cursor:pointer; border:none; }
        .btn:hover { background:#35a245; }
    </style>
</head>
<body>
<div class="card">
    <div class="icon">✅</div>
    <h1>Connectat!</h1>
    <p>Benvingut, <strong>$USER</strong>. Ja tens acces a internet.</p>
    <a href="http://www.google.com" class="btn">Comencar a navegar</a>
    <p class="info">IP: <code>$CLIENT_IP</code> · MAC: <code>$CLIENT_MAC</code></p>
</div>
</body>
</html>
EOM
else
    # Error d'autenticacio - mostrar error directament (iOS CNA no segueix meta-refresh)
    ERROR_MSG=$(echo "$RESULTAT" | sed 's/^ERROR: //')
    cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Error - Portal WiFi</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        :root { --bg-base:#0d1117; --bg-surface:#161b22; --err:#f85149; --t1:#e6edf3; --t2:#8b949e; --bd:rgba(255,255,255,0.08); --orange:#f97316; }
        *, *::before, *::after { box-sizing:border-box; margin:0; padding:0; }
        body { font-family:'Inter',system-ui,sans-serif; background:var(--bg-base); color:var(--t1); min-height:100vh; display:flex; align-items:center; justify-content:center; padding:1.5rem; }
        .card { background:var(--bg-surface); border:1px solid var(--bd); border-left:3px solid var(--orange); border-radius:12px; padding:2rem; text-align:center; max-width:400px; width:100%; }
        .icon { font-size:2.5rem; margin-bottom:1rem; }
        h1 { font-size:1.2rem; font-weight:700; margin-bottom:0.5rem; }
        .err { background:rgba(248,81,73,0.1); border:1px solid rgba(248,81,73,0.3); border-radius:8px; padding:0.65rem 0.9rem; color:#ff7b72; font-size:0.87rem; margin:1rem 0; }
        .btn { display:inline-block; padding:0.6rem 1.4rem; background:var(--orange); color:white; border-radius:8px; font-weight:700; font-family:inherit; font-size:0.9rem; text-decoration:none; margin-top:0.5rem; }
    </style>
</head>
<body>
<div class="card">
    <div class="icon">❌</div>
    <h1>Error d'autenticacio</h1>
    <div class="err">$ERROR_MSG</div>
    <a href="/cgi-bin/portal-captiu-login.cgi" class="btn">Tornar a intentar</a>
</div>
</body>
</html>
EOM
fi
