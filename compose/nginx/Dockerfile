FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf

# 删除原有配置文件，创建静态资源文件夹和ssl证书保存文件夹
RUN rm /etc/nginx/conf.d/default.conf \
&& mkdir -p /usr/share/nginx/ssl

CMD ["nginx", "-g", "daemon off;"]