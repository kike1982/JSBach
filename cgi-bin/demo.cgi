#!/bin/bash
echo "Content-Type: text/html"
echo ""
cat << 'EOF'
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JSBach — Vista previa del estilo</title>
    <link rel="stylesheet" href="/cgi-bin/style.cgi">
    <style>
        body { padding: 0; }

        .demo-wrapper {
            display: grid;
            grid-template-rows: auto 1fr;
            min-height: 100vh;
        }

        /* Barra superior */
        .topbar {
            background: var(--bg-surface);
            border-bottom: 1px solid var(--bd);
            padding: 0.6rem 1.25rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .topbar-brand {
            font-weight: 700;
            font-size: 0.95rem;
            color: var(--accent);
            letter-spacing: 0.05em;
            margin-right: 0.75rem;
            padding-right: 0.75rem;
            border-right: 1px solid var(--bd);
        }

        /* Cuerpo con sidebar */
        .main-area {
            display: grid;
            grid-template-columns: 210px 1fr;
        }
        .sidebar {
            background: var(--bg-surface);
            border-right: 1px solid var(--bd);
            padding: 1rem 0.75rem;
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }
        .sidebar-label {
            font-size: 0.69rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.09em;
            color: var(--t3);
            padding: 0.75rem 0.9rem 0.35rem;
        }
        .content-area {
            padding: 1.75rem;
            overflow: auto;
            background: var(--bg-base);
        }

        /* Nota de demo */
        .demo-notice {
            background: var(--accent-dim);
            border: 1px solid var(--bd-a);
            border-radius: var(--r);
            padding: 0.6rem 1rem;
            font-size: 0.8rem;
            color: var(--accent);
            margin-bottom: 1.5rem;
        }
    </style>
</head>
<body>
<div class="demo-wrapper">

    <!-- BARRA SUPERIOR -->
    <nav class="topbar">
        <span class="topbar-brand">JSBach</span>
        <button class="nav-btn active">Inicio</button>
        <button class="nav-btn">WAN</button>
        <button class="nav-btn">Enrutar</button>
        <button class="nav-btn">Bridge</button>
        <button class="nav-btn">Tallafocs</button>
        <button class="nav-btn">DMZ</button>
        <button class="nav-btn">Switch</button>
    </nav>

    <div class="main-area">

        <!-- SIDEBAR -->
        <aside class="sidebar">
            <div class="sidebar-label">General</div>
            <a class="menu-item active">Vista general</a>
            <a class="menu-item">Estado del sistema</a>
            <a class="menu-item">Informacion red</a>
            <div class="sidebar-label">Configuracion</div>
            <a class="menu-item">Interfaces</a>
            <a class="menu-item">Rutas</a>
            <a class="menu-item">DNS</a>
        </aside>

        <!-- CONTENIDO -->
        <main class="content-area">

            <div class="demo-notice">
                Vista previa del nuevo estilo — verifica los componentes antes de aplicar a todas las paginas
            </div>

            <!-- Cabecera -->
            <div class="page-header">
                <div>
                    <div class="page-title">Centro de Control</div>
                    <div class="page-subtitle">Estado general del router JSBach</div>
                </div>
                <span class="badge badge-ok">Sistema operativo</span>
            </div>

            <!-- TARJETAS DE MODULOS -->
            <div class="grid grid-auto mb-lg">

                <div class="card card-accent">
                    <div class="card-header">
                        <span class="card-title">WAN</span>
                        <span class="badge badge-ok">Activo</span>
                    </div>
                    <div class="info-grid">
                        <div class="info-item">
                            <div class="info-label">Interfaz</div>
                            <div class="info-value">eth0</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">IP</div>
                            <div class="info-value">192.168.1.100</div>
                        </div>
                    </div>
                    <div class="mt-sm flex gap-xs">
                        <button class="btn btn-ghost btn-sm">Ver detalles</button>
                        <button class="btn btn-danger btn-sm">Aturar</button>
                    </div>
                </div>

                <div class="card card-ok">
                    <div class="card-header">
                        <span class="card-title">Bridge</span>
                        <span class="badge badge-ok">Activo</span>
                    </div>
                    <div class="info-grid">
                        <div class="info-item">
                            <div class="info-label">VLANs</div>
                            <div class="info-value">3</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Interfaces</div>
                            <div class="info-value">br0, br10</div>
                        </div>
                    </div>
                    <div class="mt-sm flex gap-xs">
                        <button class="btn btn-ghost btn-sm">Ver detalles</button>
                        <button class="btn btn-danger btn-sm">Aturar</button>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <span class="card-title">Tallafocs</span>
                        <span class="badge badge-err">Inactivo</span>
                    </div>
                    <div class="info-grid">
                        <div class="info-item">
                            <div class="info-label">Reglas</div>
                            <div class="info-value">0</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Politica</div>
                            <div class="info-value">ACCEPT</div>
                        </div>
                    </div>
                    <div class="mt-sm flex gap-xs">
                        <button class="btn btn-ghost btn-sm">Ver detalles</button>
                        <button class="btn btn-success btn-sm">Iniciar</button>
                    </div>
                </div>

                <div class="card card-warn">
                    <div class="card-header">
                        <span class="card-title">DMZ</span>
                        <span class="badge badge-warn">Pendiente</span>
                    </div>
                    <div class="info-grid">
                        <div class="info-item">
                            <div class="info-label">Serveis</div>
                            <div class="info-value">2</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Exposats</div>
                            <div class="info-value">HTTP, SSH</div>
                        </div>
                    </div>
                    <div class="mt-sm flex gap-xs">
                        <button class="btn btn-ghost btn-sm">Ver detalles</button>
                    </div>
                </div>

            </div>

            <!-- SALIDA TERMINAL -->
            <div class="card mb-lg">
                <div class="card-header">
                    <span class="card-title">Salida del sistema</span>
                    <button class="btn btn-ghost btn-sm">Actualizar</button>
                </div>
                <div class="output output-box">eth0: flags=4163&lt;UP,BROADCAST,RUNNING,MULTICAST&gt;  mtu 1500
      inet 192.168.1.100  netmask 255.255.255.0  broadcast 192.168.1.255
      ether 00:11:22:33:44:55  txqueuelen 1000  (Ethernet)

br0: flags=4163&lt;UP,BROADCAST,RUNNING,MULTICAST&gt;  mtu 1500
      inet 10.0.0.1  netmask 255.255.255.0</div>
            </div>

            <!-- TABLA -->
            <div class="card mb-lg">
                <div class="card-header">
                    <span class="card-title">Tabla de MACs</span>
                    <span class="badge badge-info">3 entradas</span>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>MAC Address</th>
                            <th>Interfaz</th>
                            <th>VLAN</th>
                            <th>Estado</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td class="text-mono">00:11:22:33:44:55</td>
                            <td>eth0</td>
                            <td>10</td>
                            <td><span class="badge badge-ok">Activo</span></td>
                        </tr>
                        <tr>
                            <td class="text-mono">aa:bb:cc:dd:ee:ff</td>
                            <td>eth1</td>
                            <td>20</td>
                            <td><span class="badge badge-ok">Activo</span></td>
                        </tr>
                        <tr>
                            <td class="text-mono">11:22:33:44:55:66</td>
                            <td>eth2</td>
                            <td>—</td>
                            <td><span class="badge badge-muted">Inactivo</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- FORMULARIO + ALERTAS -->
            <div class="grid grid-2 mb-lg">

                <div class="card">
                    <div class="card-header">
                        <span class="card-title">Configuracion WAN</span>
                    </div>
                    <div class="form-group">
                        <label>Interfaz</label>
                        <select>
                            <option>eth0</option>
                            <option>eth1</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Direccion IP</label>
                        <input type="text" placeholder="192.168.1.1">
                    </div>
                    <div class="form-group">
                        <label>Mascara de red</label>
                        <input type="text" placeholder="255.255.255.0">
                    </div>
                    <div class="flex gap-sm">
                        <button class="btn btn-primary">Guardar</button>
                        <button class="btn btn-ghost">Cancelar</button>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <span class="card-title">Alertas y mensajes</span>
                    </div>
                    <div class="alert alert-ok">Configuracion guardada correctamente</div>
                    <div class="alert alert-warn">El servicio WAN no esta iniciado</div>
                    <div class="alert alert-err">Error al aplicar reglas de firewall</div>
                    <div class="alert alert-info">Activa el forwarding IP para el routing</div>

                    <hr class="divider">

                    <details>
                        <summary>Ver detalles tecnicos</summary>
                        <div class="output" style="margin-top:0.5rem">iptables -L -n -v
Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
Chain FORWARD (policy DROP 0 packets, 0 bytes)
Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)</div>
                    </details>

                    <details>
                        <summary>Informacion del sistema</summary>
                        <div class="info-grid">
                            <div class="info-item">
                                <div class="info-label">Uptime</div>
                                <div class="info-value">3d 14h</div>
                            </div>
                            <div class="info-item">
                                <div class="info-label">Carga</div>
                                <div class="info-value">0.12</div>
                            </div>
                            <div class="info-item">
                                <div class="info-label">Memoria</div>
                                <div class="info-value">312 MB</div>
                            </div>
                        </div>
                    </details>
                </div>

            </div>

        </main>
    </div>
</div>
</body>
</html>
EOF
