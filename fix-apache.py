#!/usr/bin/env python3
conf = '/etc/apache2/sites-enabled/000-default.conf'
lines = [
    '    RewriteEngine On',
    r'    RewriteCond %{REMOTE_ADDR} ^192\.168\.100\.[0-9]+$',
    r'    RewriteCond %{REQUEST_URI} !^/cgi-bin/portal-captiu',
    '    RewriteRule ^ /cgi-bin/portal-captiu-login.cgi [R=302,L]',
]
insert = '\n'.join(lines) + '\n'
c = open(conf).read()
if 'RewriteEngine On' in c:
    print('Ya tiene RewriteEngine, no se modifica')
else:
    c = c.replace('</VirtualHost>', insert + '</VirtualHost>')
    open(conf, 'w').write(c)
    print('OK')
