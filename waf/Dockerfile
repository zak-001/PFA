FROM debian:bookworm

RUN apt-get update && \
    apt-get install -y nginx libnginx-mod-security modsecurity-crs && \
    apt-get clean

COPY modsecurity.conf /etc/modsecurity/
COPY nginx.conf /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]

#configure ModSecurity rules in modsecurity.conf and integrate it with Nginx via nginx.conf
