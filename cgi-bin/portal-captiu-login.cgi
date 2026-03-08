#!/bin/bash

echo "Content-type: text/html; charset=utf-8"
echo ""

MSG=$(echo "$QUERY_STRING" | sed -n 's/^.*msg=\([^&]*\).*$/\1/p' | sed 's/+/ /g; s/%20/ /g; s/%3A/:/g')

cat << 'ENDCSS'
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portal WiFi - Acces a internet</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        :root {
            --bg-base: #0d1117;
            --bg-surface: #161b22;
            --bg-raise: #21262d;
            --accent: #22d3ee;
            --accent-dim: rgba(34,211,238,0.12);
            --ok: #3fb950;
            --err: #f85149;
            --t1: #e6edf3;
            --t2: #8b949e;
            --t3: #6e7681;
            --bd: rgba(255,255,255,0.08);
            --r: 8px;
            --orange: #f97316;
        }
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Inter', system-ui, sans-serif;
            background: var(--bg-base);
            color: var(--t1);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1.5rem;
        }
        .login-wrapper {
            width: 100%;
            max-width: 420px;
        }
        .login-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        .login-logo {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        .login-title {
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--t1);
        }
        .login-subtitle {
            font-size: 0.88rem;
            color: var(--t2);
            margin-top: 0.35rem;
        }
        .login-card {
            background: var(--bg-surface);
            border: 1px solid var(--bd);
            border-left: 3px solid var(--orange);
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 8px 24px rgba(0,0,0,0.6);
        }
        label {
            display: block;
            font-size: 0.82rem;
            font-weight: 600;
            color: var(--t2);
            margin-bottom: 0.35rem;
        }
        input[type="text"], input[type="password"] {
            width: 100%;
            background: var(--bg-base);
            border: 1px solid var(--bd);
            border-radius: var(--r);
            padding: 0.55rem 0.8rem;
            color: var(--t1);
            font-size: 0.9rem;
            font-family: inherit;
            outline: none;
            transition: border-color 0.17s;
        }
        input:focus { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-dim); }
        .form-group { margin-bottom: 1.1rem; }
        .btn-login {
            width: 100%;
            padding: 0.65rem;
            background: var(--accent);
            color: #0d1117;
            border: none;
            border-radius: var(--r);
            font-size: 0.95rem;
            font-weight: 700;
            font-family: inherit;
            cursor: pointer;
            transition: background 0.17s;
            margin-top: 0.5rem;
        }
        .btn-login:hover { background: #67e8f9; }
        .alert-err {
            background: rgba(248,81,73,0.1);
            border: 1px solid rgba(248,81,73,0.3);
            border-left: 3px solid var(--err);
            border-radius: var(--r);
            padding: 0.65rem 0.9rem;
            color: #ff7b72;
            font-size: 0.87rem;
            margin-bottom: 1.1rem;
        }
        .footer-note {
            text-align: center;
            font-size: 0.78rem;
            color: var(--t3);
            margin-top: 1.25rem;
        }
    </style>
</head>
<body>
<div class="login-wrapper">
    <div class="login-header">
        <div class="login-logo">📶</div>
        <div class="login-title">Portal WiFi</div>
        <div class="login-subtitle">Introdueix les teves credencials per accedir a internet</div>
    </div>
    <div class="login-card">
ENDCSS

if [[ -n "$MSG" ]]; then
    echo "        <div class='alert-err'>$MSG</div>"
fi

cat << 'EOF'
        <form action="/cgi-bin/portal-captiu-auth.cgi" method="get">
            <div class="form-group">
                <label for="user">Usuari</label>
                <input type="text" id="user" name="user" placeholder="Nom d'usuari" autocomplete="username" required autofocus>
            </div>
            <div class="form-group">
                <label for="pass">Contrasenya</label>
                <input type="password" id="pass" name="pass" placeholder="Contrasenya" autocomplete="current-password" required>
            </div>
            <button type="submit" class="btn-login">Connectar</button>
        </form>
    </div>
    <p class="footer-note">JSBach Router · Portal captiu</p>
</div>
</body>
</html>
EOF
