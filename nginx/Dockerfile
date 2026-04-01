FROM nginx:latest
EXPOSE 80
ADD ./djsite.conf /etc/nginx/conf.d/djsite.conf

CMD ["nginx", "-g", "daemon off;"]
# for foreground process