#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

int=$(echo "$QUERY_STRING" | sed -n 's/^.*int=\([^&]*\).*$/\1/p')

VLAN_DATA="$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge configurar mostrar bridge)"
linia_int=$(echo "$VLAN_DATA" | grep -E "^${int};")
VLAN_UNTAG=$(echo "$linia_int" | cut -d';' -f2)
VLAN_TAG=$(echo "$linia_int" | cut -d';' -f3)

cat << EOM
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="utf-8">
    <title>Modificar Tag-Untag</title>
    <style>
        /* --- Estil Modern Dark --- */
        body {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background: #0f172a;
            color: #f8fafc;
            margin: 0;
            padding: 24px;
            line-height: 1.6;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        h2 {
            text-align: center;
            color: #3b82f6;
            margin-bottom: 30px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .card {
            background: #1e293b;
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        }
        .card-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 20px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            padding-bottom: 12px;
        }
        .card-title {
            font-size: 1.1rem;
            font-weight: 700;
            color: #94a3b8;
            margin: 0;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #cbd5e1;
            font-size: 0.9rem;
        }
        input[type="text"] {
            width: 100%;
            padding: 12px;
            background: #0f172a;
            border: 1px solid #334155;
            border-radius: 8px;
            color: #f8fafc;
            font-family: 'Fira Code', monospace;
            transition: all 0.2s;
            box-sizing: border-box;
        }
        input[type="text"]:focus {
            outline: none;
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
        }
        input[readonly] {
            background: #1e293b;
            color: #64748b;
            cursor: not-allowed;
            border-style: dashed;
        }
        .btn-group {
            display: flex;
            gap: 15px;
            margin-top: 32px;
        }
        .btn {
            flex: 1;
            padding: 14px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 700;
            font-size: 1rem;
            transition: all 0.2s;
            text-transform: uppercase;
            letter-spacing: 0.025em;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            text-decoration: none;
        }
        .btn-submit { background: #3b82f6; color: white; }
        .btn-submit:hover { background: #2563eb; transform: translateY(-1px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3); }
        .btn-back { background: #475569; color: white; }
        .btn-back:hover { background: #334155; transform: translateY(-1px); }
        .footer {
            text-align: center;
            margin-top: 40px;
            font-size: 0.8rem;
            color: #64748b;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>🏷️ Modificar Tag-Untag</h2>
        <form action='/cgi-bin/bridge-guardar-taguntag.cgi' method='get'>
            <div class="card">
                <div class="card-header"><h3 class="card-title">🔌 Interfaç de Xarxa</h3></div>
                <div class="form-group">
                    <label>Nom de l'interfaç:</label>
                    <input type="text" name="int" value="$int" readonly>
                </div>
            </div>

            <div class="card">
                <div class="card-header"><h3 class="card-title">🏷️ Configuració VLAN</h3></div>
                <div class="form-group">
                    <label>VLAN UNTAG (PVID):</label>
                    <input type="text" name="untag" value="$VLAN_UNTAG" 
                           pattern="^[0-9]+$" required 
                           title="Només números. 0 si no hi ha VLAN untagged.">
                </div>
                <div class="form-group">
                    <label>VLANs TAGGED:</label>
                    <input type="text" name="tag" value="$VLAN_TAG" 
                           pattern="^[0-9]+(-[0-9]+)?(,[0-9]+(-[0-9]+)?)*$" required
                           title="Llista de VLANs. Exemple: 10,20 o rangs 10-20 o combinat 10-20,30,40-45">
                </div>
            </div>

            <div class="btn-group">
                <a href="/cgi-bin/bridge-configurar-taguntag.cgi" class="btn btn-back">⬅️ Tornar</a>
                <button type="submit" class="btn btn-submit">💾 Guardar Canvis</button>
            </div>
        </form>
        <div class='footer'>Gestió de xarxes © 2026</div>
    </div>
</body>
</html>
EOM
