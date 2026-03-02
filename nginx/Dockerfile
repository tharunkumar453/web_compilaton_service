FROM nginx:latest
EXPOSE 443
ADD ./djsite.conf /etc/nginx/conf.d/djsite.conf
ADD  ./nginx-selfsigned.crt /etc/ssl/certs/
ADD  ./ssl.key /etc/ssl/private/
CMD ["nginx", "-g", "daemon off;"]