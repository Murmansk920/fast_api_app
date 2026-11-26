FROM nginx:1.27-alpine

# 删除默认配置
RUN rm /etc/nginx/conf.d/default.conf

# 拷贝自定义 nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 拷贝前端静态文件
COPY html/ /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]