#!/bin/bash
printf "Content-Type: text/css\n\n"
cat << 'ENDCSS'
/* ============================================================
   JSBach Router Admin — Hoja de estilo global
   ============================================================ */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* --- Variables -------------------------------------------- */
:root {
    --bg-base:    #0d1117;
    --bg-surface: #161b22;
    --bg-raise:   #21262d;
    --bg-hover:   #2d333b;

    --accent:     #22d3ee;
    --accent-dim: rgba(34, 211, 238, 0.12);
    --accent-dark:#0e7490;

    --ok:   #3fb950;
    --warn: #d29922;
    --err:  #f85149;

    --t1: #e6edf3;
    --t2: #8b949e;
    --t3: #6e7681;

    --bd:   rgba(255, 255, 255, 0.08);
    --bd-a: rgba(34, 211, 238, 0.25);

    --r:    8px;
    --r-lg: 12px;

    --sh:    0 2px 8px rgba(0, 0, 0, 0.45);
    --sh-lg: 0 8px 24px rgba(0, 0, 0, 0.6);

    --ease: 0.17s ease;
}

/* --- Reset & Base ----------------------------------------- */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { font-size: 15px; }
body {
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg-base);
    color: var(--t1);
    line-height: 1.6;
    min-height: 100vh;
    padding: 1.5rem;
}
body.no-pad { padding: 0; }

/* --- Tipografia ------------------------------------------- */
h1 { font-size: 1.4rem; font-weight: 700; }
h2 { font-size: 1.15rem; font-weight: 700; }
h3 { font-size: 1rem; font-weight: 600; }
h1, h2, h3 { line-height: 1.3; color: var(--t1); }
p { color: var(--t2); }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
code, pre, kbd, .mono {
    font-family: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;
}

/* --- Layout ----------------------------------------------- */
.container { max-width: 1100px; margin: 0 auto; width: 100%; }
.grid      { display: grid; gap: 1.25rem; }
.grid-2    { grid-template-columns: repeat(2, 1fr); }
.grid-3    { grid-template-columns: repeat(3, 1fr); }
.grid-auto { grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); }

/* --- Cards ------------------------------------------------ */
.card {
    background: var(--bg-surface);
    border: 1px solid var(--bd);
    border-radius: var(--r-lg);
    padding: 1.4rem;
    box-shadow: var(--sh);
    transition: border-color var(--ease), box-shadow var(--ease);
}
.card:hover {
    border-color: rgba(34, 211, 238, 0.18);
    box-shadow: var(--sh-lg);
}
.card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    padding-bottom: 0.9rem;
    margin-bottom: 0.9rem;
    border-bottom: 1px solid var(--bd);
}
.card-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--t1);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.card-accent { border-left: 3px solid var(--accent); }
.card-ok     { border-left: 3px solid var(--ok); }
.card-err    { border-left: 3px solid var(--err); }
.card-warn   { border-left: 3px solid var(--warn); }

/* --- Botones ---------------------------------------------- */
.btn {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.48rem 1rem;
    border-radius: var(--r);
    font-size: 0.84rem;
    font-weight: 600;
    cursor: pointer;
    border: 1px solid transparent;
    transition: all var(--ease);
    text-decoration: none;
    white-space: nowrap;
    font-family: inherit;
}
.btn:hover  { transform: translateY(-1px); text-decoration: none; }
.btn:active { transform: translateY(0); }

.btn-primary { background: var(--accent); color: #0d1117; border-color: var(--accent); }
.btn-primary:hover { background: #67e8f9; border-color: #67e8f9; }

.btn-ghost { background: transparent; color: var(--t2); border-color: var(--bd); }
.btn-ghost:hover { background: var(--bg-hover); color: var(--t1); border-color: var(--bd-a); }

.btn-danger  { background: var(--err);  color: white;   border-color: var(--err); }
.btn-success { background: var(--ok);   color: white;   border-color: var(--ok); }
.btn-warn    { background: var(--warn); color: #0d1117; border-color: var(--warn); }

.btn-sm    { padding: 0.28rem 0.7rem; font-size: 0.77rem; }
.btn-lg    { padding: 0.6rem 1.4rem;  font-size: 0.92rem; }
.btn-block { width: 100%; justify-content: center; }

/* --- Nav buttons ------------------------------------------ */
.nav-btn {
    padding: 0.42rem 0.95rem;
    background: transparent;
    border: 1px solid var(--bd);
    border-radius: var(--r);
    color: var(--t2);
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    cursor: pointer;
    transition: all var(--ease);
    font-family: inherit;
}
.nav-btn:hover { background: var(--accent-dim); border-color: var(--bd-a); color: var(--accent); }
.nav-btn.active, .nav-btn.btn-active {
    background: var(--accent-dim);
    border-color: var(--accent);
    color: var(--accent);
}

/* --- Badges ----------------------------------------------- */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.2rem 0.65rem;
    border-radius: 99px;
    font-size: 0.71rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border: 1px solid;
}
.badge::before {
    content: '';
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: currentColor;
    flex-shrink: 0;
}
.badge-ok, .badge-active    { background: rgba(63,185,80,0.12);  color: #5cb85c; border-color: rgba(63,185,80,0.3); }
.badge-err, .badge-inactive  { background: rgba(248,81,73,0.12);  color: #f87171; border-color: rgba(248,81,73,0.3); }
.badge-warn                  { background: rgba(210,153,34,0.12); color: #d29922; border-color: rgba(210,153,34,0.3); }
.badge-info                  { background: var(--accent-dim); color: var(--accent); border-color: var(--bd-a); }
.badge-muted                 { background: rgba(110,118,129,0.12); color: var(--t3); border-color: rgba(110,118,129,0.3); }

/* --- Terminal output -------------------------------------- */
.output {
    background: #010409;
    border: 1px solid var(--bd);
    border-radius: var(--r);
    padding: 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.81rem;
    color: #7ee787;
    white-space: pre-wrap;
    word-break: break-all;
    overflow-x: auto;
    line-height: 1.75;
}
.output-box { border-left: 3px solid var(--accent); color: #e6edf3; }

/* --- Tablas ----------------------------------------------- */
table { width: 100%; border-collapse: collapse; font-size: 0.87rem; }
thead th {
    text-align: left;
    color: var(--t3);
    font-size: 0.73rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    padding: 0.55rem 0.8rem;
    border-bottom: 1px solid var(--bd);
}
tbody td {
    padding: 0.55rem 0.8rem;
    border-bottom: 1px solid var(--bd);
    color: var(--t2);
    vertical-align: middle;
}
tbody tr:last-child td { border-bottom: none; }
tbody tr:hover td { background: var(--bg-raise); color: var(--t1); }

/* --- Formularios ------------------------------------------ */
label { display: block; font-size: 0.82rem; font-weight: 600; color: var(--t2); margin-bottom: 0.35rem; }
input[type="text"],
input[type="number"],
input[type="password"],
input[type="email"],
select,
textarea {
    width: 100%;
    background: var(--bg-base);
    border: 1px solid var(--bd);
    border-radius: var(--r);
    padding: 0.48rem 0.75rem;
    color: var(--t1);
    font-size: 0.87rem;
    font-family: inherit;
    transition: border-color var(--ease), box-shadow var(--ease);
    outline: none;
    appearance: none;
}
input:focus, select:focus, textarea:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px var(--accent-dim);
}
.form-group { margin-bottom: 1.1rem; }
.form-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; }

/* --- Cabecera de pagina ----------------------------------- */
.page-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 1.75rem;
    padding-bottom: 1.1rem;
    border-bottom: 1px solid var(--bd);
}
.page-title    { font-size: 1.25rem; font-weight: 700; color: var(--t1); }
.page-subtitle { font-size: 0.83rem; color: var(--t3); margin-top: 0.2rem; }

/* --- Menu lateral ----------------------------------------- */
.menu-item {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    padding: 0.6rem 0.9rem;
    border-radius: var(--r);
    font-size: 0.87rem;
    font-weight: 500;
    color: var(--t2);
    text-decoration: none;
    cursor: pointer;
    transition: all var(--ease);
    border: 1px solid transparent;
}
.menu-item:hover {
    background: var(--bg-raise);
    border-color: var(--bd);
    color: var(--t1);
    transform: translateX(2px);
    text-decoration: none;
}
.menu-item.active { background: var(--accent-dim); border-color: var(--bd-a); color: var(--accent); }

/* --- Alertas ---------------------------------------------- */
.alert {
    padding: 0.7rem 1rem;
    border-radius: var(--r);
    font-size: 0.87rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
    border-left: 3px solid;
}
.alert-ok   { background: rgba(63,185,80,0.1);  border-color: var(--ok);     color: #7ee787; }
.alert-err  { background: rgba(248,81,73,0.1);  border-color: var(--err);    color: #ff7b72; }
.alert-warn { background: rgba(210,153,34,0.1); border-color: var(--warn);   color: #d29922; }
.alert-info { background: var(--accent-dim);    border-color: var(--accent); color: var(--accent); }

/* --- Details/Summary -------------------------------------- */
details { border: 1px solid var(--bd); border-radius: var(--r); margin-bottom: 0.75rem; overflow: hidden; }
summary {
    padding: 0.7rem 1rem;
    cursor: pointer;
    font-weight: 600;
    font-size: 0.87rem;
    color: var(--t2);
    background: var(--bg-surface);
    list-style: none;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: background var(--ease);
    user-select: none;
}
summary::-webkit-details-marker { display: none; }
summary::after { content: '+'; font-size: 1.1rem; color: var(--t3); }
details[open] summary::after { content: '-'; }
details[open] summary { border-bottom: 1px solid var(--bd); }
summary:hover { background: var(--bg-raise); color: var(--t1); }
details > *:not(summary) { padding: 1rem; }

/* --- Separador -------------------------------------------- */
.divider, hr { border: none; border-top: 1px solid var(--bd); margin: 1.1rem 0; }

/* --- Info grid -------------------------------------------- */
.info-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 1rem; margin-top: 0.5rem; }
.info-label { font-size: 0.72rem; color: var(--t3); text-transform: uppercase; font-weight: 600; letter-spacing: 0.06em; margin-bottom: 0.2rem; }
.info-value { font-size: 0.92rem; font-weight: 600; color: var(--t1); }

/* --- Utilidades ------------------------------------------- */
.text-accent  { color: var(--accent); }
.text-ok      { color: var(--ok); }
.text-err     { color: var(--err); }
.text-warn    { color: var(--warn); }
.text-muted   { color: var(--t2); }
.text-dimmed  { color: var(--t3); }
.text-right   { text-align: right; }
.text-center  { text-align: center; }
.text-small   { font-size: 0.82rem; }
.text-mono    { font-family: 'JetBrains Mono', monospace; }
.fw-bold      { font-weight: 700; }

.flex         { display: flex; }
.flex-center  { display: flex; align-items: center; }
.flex-between { display: flex; align-items: center; justify-content: space-between; }
.flex-wrap    { flex-wrap: wrap; }
.gap-xs { gap: 0.35rem; }
.gap-sm { gap: 0.6rem; }
.gap-md { gap: 1rem; }
.gap-lg { gap: 1.5rem; }

.mt-xs { margin-top: 0.35rem; }
.mt-sm { margin-top: 0.6rem; }
.mt-md { margin-top: 1rem; }
.mt-lg { margin-top: 1.5rem; }
.mb-xs { margin-bottom: 0.35rem; }
.mb-sm { margin-bottom: 0.6rem; }
.mb-md { margin-bottom: 1rem; }
.mb-lg { margin-bottom: 1.5rem; }

.w-full { width: 100%; }
.hidden { display: none !important; }

/* --- Responsive ------------------------------------------- */
@media (max-width: 768px) {
    body { padding: 1rem; }
    .grid-2, .grid-3 { grid-template-columns: 1fr; }
    .page-header { flex-direction: column; align-items: flex-start; }
}

/* --- Compatibilidad (clases de páginas existentes) -------- */

/* Status badges (info.cgi, switch.cgi) */
.status-badge {
    display: inline-flex; align-items: center; gap: 0.3rem;
    padding: 0.2rem 0.65rem; border-radius: 99px;
    font-size: 0.71rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.05em; border: 1px solid;
}
.status-active   { background: rgba(63,185,80,0.12);   color: #5cb85c;      border-color: rgba(63,185,80,0.3); }
.status-inactive { background: rgba(110,118,129,0.12); color: var(--t3);    border-color: rgba(110,118,129,0.3); }
.status-down     { background: rgba(248,81,73,0.12);   color: #f87171;      border-color: rgba(248,81,73,0.3); }

/* Tarjetas por módulo (info.cgi) */
.card-wan       { border-left: 3px solid var(--accent); }
.card-enrutar   { border-left: 3px solid var(--ok); }
.card-bridge    { border-left: 3px solid var(--warn); }
.card-tallafocs { border-left: 3px solid var(--err); }
.card-dmz       { border-left: 3px solid #a855f7; }
.card-switch    { border-left: 3px solid var(--warn); }

/* Badges adicionales */
.badge-conn     { background: rgba(63,185,80,0.12);   color: #5cb85c; border-color: rgba(63,185,80,0.3); }
.badge-desconn  { background: rgba(248,81,73,0.12);   color: #f87171; border-color: rgba(248,81,73,0.3); }
.badge-wls      { background: rgba(210,153,34,0.12);  color: #d29922; border-color: rgba(210,153,34,0.3); }
.badge-ailla    { background: rgba(248,81,73,0.12);   color: #f87171; border-color: rgba(248,81,73,0.3); }
.badge-open     { background: rgba(63,185,80,0.12);   color: #5cb85c; border-color: rgba(63,185,80,0.3); }
.badge-blocked  { background: rgba(248,81,73,0.12);   color: #f87171; border-color: rgba(248,81,73,0.3); }
.badge-isolated { background: rgba(248,81,73,0.12);   color: #f87171; border-color: rgba(248,81,73,0.3); }
.badge-normal   { background: rgba(63,185,80,0.12);   color: #5cb85c; border-color: rgba(63,185,80,0.3); }
.badge-manual   { background: rgba(110,118,129,0.12); color: var(--t3); border-color: rgba(110,118,129,0.3); }
.badge-dhcp     { background: var(--accent-dim); color: var(--accent); border-color: var(--bd-a); }
.badge-proto    { background: var(--accent-dim); color: var(--accent); border-color: var(--bd-a); }

/* Botones alias */
.btn-submit     { background: var(--accent); color: #0d1117; border-color: var(--accent); }
.btn-submit:hover { background: #67e8f9; border-color: #67e8f9; }
.btn-back       { background: transparent; color: var(--t2); border-color: var(--bd); }
.btn-back:hover { background: var(--bg-hover); color: var(--t1); border-color: var(--bd-a); }
.btn-edit       { background: transparent; color: var(--t2); border-color: var(--bd); }
.btn-edit:hover { background: var(--bg-hover); color: var(--t1); border-color: var(--bd-a); }
.btn-delete     { background: var(--err);  color: white; border-color: var(--err); }
.btn-delete:hover { background: #e03c37; }
.btn-create     { background: var(--accent); color: #0d1117; border-color: var(--accent); }
.btn-create:hover { background: #67e8f9; border-color: #67e8f9; }
.btn-connect    { background: var(--ok);   color: white; border-color: var(--ok); }
.btn-connect:hover { background: #35a245; }
.btn-disconnect { background: var(--err);  color: white; border-color: var(--err); }
.btn-disconnect:hover { background: #e03c37; }
.btn-isolate    { background: var(--warn); color: #0d1117; border-color: var(--warn); }
.btn-isolate:hover { background: #c08c1a; }
.btn-unisolate  { background: var(--ok);   color: white; border-color: var(--ok); }
.btn-unisolate:hover { background: #35a245; }
.btn-view {
    display: inline-flex; align-items: center; gap: 0.4rem;
    padding: 0.28rem 0.7rem; border-radius: var(--r);
    font-size: 0.77rem; font-weight: 600; cursor: pointer;
    border: 1px solid var(--bd); background: transparent;
    color: var(--t2); transition: all var(--ease); font-family: inherit;
}
.btn-view:hover { background: var(--bg-hover); color: var(--t1); }
.btn-group { display: flex; gap: 0.5rem; flex-wrap: wrap; align-items: center; }

/* Alertas alias (switch-config, switch-macs) */
.msg         { padding: 0.7rem 1rem; border-radius: var(--r); font-size: 0.87rem; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.6rem; border-left: 3px solid; }
.msg-success { background: rgba(63,185,80,0.1);  border-color: var(--ok);     color: #7ee787; }
.msg-error   { background: rgba(248,81,73,0.1);  border-color: var(--err);    color: #ff7b72; }
.msg-warning { background: rgba(210,153,34,0.1); border-color: var(--warn);   color: #d29922; }
.msg-info    { background: var(--accent-dim);    border-color: var(--accent); color: var(--accent); }

/* Cajas de error/advertencia */
.error-box   { background: rgba(248,81,73,0.1);  border: 1px solid rgba(248,81,73,0.3);  border-left: 3px solid var(--err);  border-radius: var(--r); padding: 0.7rem 1rem; color: #ff7b72; margin-bottom: 1rem; }
.warning-box { background: rgba(210,153,34,0.1); border: 1px solid rgba(210,153,34,0.3); border-left: 3px solid var(--warn); border-radius: var(--r); padding: 0.7rem 1rem; color: #d29922; margin-bottom: 1rem; }

/* Output box con estado */
.output-box.success { border-left-color: var(--ok);  color: #7ee787; }
.output-box.error   { border-left-color: var(--err); color: #ff7b72; }

/* VLAN / Bridge */
.vlan-row { display: flex; align-items: center; justify-content: space-between; padding: 0.6rem 0; border-bottom: 1px solid var(--bd); gap: 0.75rem; }
.vlan-row:last-child { border-bottom: none; }
.vlan-info { display: flex; align-items: center; gap: 0.75rem; flex: 1; }
.vlan-name { font-weight: 600; color: var(--t1); }
.vlan-vid  { font-size: 0.78rem; color: var(--t3); font-family: 'JetBrains Mono', monospace; }
.vlan-net  { font-size: 0.82rem; color: var(--t2); font-family: 'JetBrains Mono', monospace; }
.vlan-badge { display: inline-flex; align-items: center; padding: 0.15rem 0.55rem; border-radius: 99px; font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; border: 1px solid; }
.iface-name { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: var(--accent); }

/* Tallafocs */
.info-group { margin-bottom: 1.25rem; }
.label      { font-size: 0.78rem; font-weight: 600; color: var(--t3); text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.25rem; }
.sublabel   { font-size: 0.75rem; color: var(--t3); }
.add-section { margin-top: 1.25rem; padding-top: 1rem; border-top: 1px solid var(--bd); }
.status-row  { display: flex; align-items: center; justify-content: space-between; padding: 0.45rem 0; gap: 0.5rem; }

/* Formularios radio */
.radio-group { display: flex; flex-direction: column; gap: 0.5rem; margin: 0.5rem 0; }
.radio-item  { display: flex; align-items: center; gap: 0.5rem; font-size: 0.87rem; color: var(--t2); cursor: pointer; }
.radio-item input[type="radio"] { width: auto; cursor: pointer; accent-color: var(--accent); }

/* Páginas de resultado */
.redirect-text { color: var(--t3); font-size: 0.83rem; margin-top: 0.75rem; }
.icon          { font-size: 2rem; line-height: 1; }
.success-icon  { font-size: 3rem; line-height: 1; }
.simple-output { background: #010409; border: 1px solid var(--bd); border-radius: var(--r); padding: 1rem; font-family: 'JetBrains Mono', monospace; font-size: 0.81rem; color: #7ee787; white-space: pre-wrap; word-break: break-all; overflow-x: auto; line-height: 1.75; }

/* cos-admin.cgi */
.header-panel { background: var(--bg-surface); border-bottom: 1px solid var(--bd); padding: 0.75rem 1rem; }
.system-info  { display: grid; gap: 0.6rem; padding: 0.5rem 0; }
.info-item    { display: flex; flex-direction: column; gap: 0.15rem; }
.module-card  { background: var(--bg-surface); border: 1px solid var(--bd); border-radius: var(--r); padding: 0.75rem 1rem; margin-bottom: 0.5rem; }

/* Menús laterales */
.menu-container { padding: 0.5rem 0; }
.menu-title  { font-size: 0.69rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.09em; color: var(--t3); padding: 0.75rem 0.9rem 0.35rem; }
.menu-list   { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 0.25rem; }
.menu-list li a { display: flex; align-items: center; gap: 0.7rem; padding: 0.6rem 0.9rem; border-radius: var(--r); font-size: 0.87rem; font-weight: 500; color: var(--t2); text-decoration: none; transition: all var(--ease); border: 1px solid transparent; }
.menu-list li a:hover { background: var(--bg-raise); border-color: var(--bd); color: var(--t1); text-decoration: none; }

/* Acciones en cabecera (dmz.cgi) */
.header-actions { display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap; }

/* Switch */
.form-grid    { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; }
.mac-item     { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: var(--t1); }
.input-group  { margin-bottom: 1.1rem; }
.input-field  { width: 100%; background: var(--bg-base); border: 1px solid var(--bd); border-radius: var(--r); padding: 0.48rem 0.75rem; color: var(--t1); font-size: 0.87rem; font-family: inherit; transition: border-color var(--ease); outline: none; }
.input-field:focus { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-dim); }
.form-card    { background: var(--bg-surface); border: 1px solid var(--bd); border-radius: var(--r-lg); padding: 1.4rem; box-shadow: var(--sh); max-width: 520px; margin-bottom: 1.5rem; }
.actions-panel { display: flex; gap: 0.75rem; align-items: center; flex-wrap: wrap; margin-bottom: 1.5rem; padding: 1rem; background: var(--bg-surface); border-radius: var(--r); border: 1px solid var(--bd); }
.details      { background: rgba(0,0,0,0.3); padding: 1rem; border-radius: var(--r); margin-top: 1rem; font-size: 0.87rem; color: var(--t2); }

/* pre (salida terminal en switch) */
pre { font-family: 'JetBrains Mono', monospace; font-size: 0.81rem; background: #010409; border: 1px solid var(--bd); border-radius: var(--r); padding: 1rem; color: #7ee787; white-space: pre-wrap; word-break: break-all; overflow-x: auto; line-height: 1.75; margin: 0.5rem 0; }

/* h4 a (archivos de menú) */
h4 { color: var(--t1); font-size: 0.95rem; font-weight: 600; margin: 0.75rem 0 0.35rem; }
h4 a { color: var(--accent); text-decoration: none; }
h4 a:hover { text-decoration: underline; }

/* Select con flecha */
select { background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%238b949e' d='M6 8L1 3h10z'/%3E%3C/svg%3E"); background-repeat: no-repeat; background-position: right 0.75rem center; padding-right: 2rem; }

/* Inputs de solo lectura */
input[readonly], select[disabled] { opacity: 0.6; cursor: not-allowed; }
ENDCSS
