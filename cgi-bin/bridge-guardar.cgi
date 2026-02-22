#!/bin/bash

source /usr/local/JSBach/conf/variables.conf
RUTA="$DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli"

urldecode() {
    local data="${1//+/ }"
    printf '%b' "${data//%/\\x}"
}

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="utf-8">
    <title>Resultat Operació</title>
    <style>
        /* --- Estil Modern Dark --- */
        body {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background: #0f172a;
            color: #f8fafc;
            margin: 0;
            padding: 24px;
            line-height: 1.6;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }
        .container {
            max-width: 700px;
            width: 100%;
        }
        h2 {
            text-align: center;
            color: #f8fafc;
            margin-bottom: 30px;
            font-weight: 800;
        }
        .card {
            background: #1e293b;
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 32px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
            text-align: center;
        }
        .output-box {
            background: #0f172a;
            border-radius: 8px;
            padding: 20px;
            font-family: 'Fira Code', monospace;
            font-size: 0.9rem;
            color: #e2e8f0;
            white-space: pre-wrap;
            border-left: 4px solid #3b82f6;
            text-align: left;
            margin-top: 20px;
        }
        .redirect-text {
            margin-top: 20px;
            color: #94a3b8;
            font-size: 0.9rem;
        }
        .success-icon {
            font-size: 4rem;
            margin-bottom: 20px;
            display: block;
        }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-top: 20px;
            text-align: left;
            font-size: 0.9rem;
        }
        .info-item {
            background: rgba(255,255,255,0.05);
            padding: 10px;
            border-radius: 6px;
        }
        .info-label { color: #64748b; font-weight: 600; display: block; margin-bottom: 4px; }
        .info-value { color: #3b82f6; font-weight: 700; }
    </style>
    <script>
        setTimeout(() => {
            window.location.href = '/cgi-bin/bridge-configurar.cgi';
        }, 3000);
    </script>
</head>
<body>
    <div class="container">
        <div class="card">
            <span class="success-icon">✅</span>
            <h2>Operació Completada</h2>
EOM

# ----------------------------------------------------
# Obtener parámetros
# ----------------------------------------------------
nom=$(echo "$QUERY_STRING" | sed -n 's/^.*nom=\([^&]*\).*$/\1/p')
vid=$(echo "$QUERY_STRING" | sed -n 's/^.*vid=\([^&]*\).*$/\1/p')
ipmasc=$(echo "$QUERY_STRING" | sed -n 's/^.*ipmasc=\([^&]*\).*$/\1/p')
ippe=$(echo "$QUERY_STRING" | sed -n 's/^.*ippe=\([^&]*\).*$/\1/p')

nom=$(urldecode "$nom")
ipmasc=$(urldecode "$ipmasc")
ippe=$(urldecode "$ippe")

cat << EOM
            <div class="info-grid">
                <div class="info-item"><span class="info-label">Nom</span><span class="info-value">$nom</span></div>
                <div class="info-item"><span class="info-label">VID</span><span class="info-value">$vid</span></div>
                <div class="info-item"><span class="info-label">Xarxa</span><span class="info-value">$ipmasc</span></div>
                <div class="info-item"><span class="info-label">Gateway</span><span class="info-value">$ippe</span></div>
            </div>

            <div class="output-box">
$($RUTA bridge configurar guardar vlan "$nom" "$vid" "$ipmasc" "$ippe")
            </div>

            <div class="redirect-text">
                Redirigint a la gestió de VLANs en 3 segons...
            </div>
        </div>
    </div>
</body>
</html>
EOM
