FROM  redis:7-alpine
WORKDIR /app
ADD redis.conf  ./redis.conf
EXPOSE 6379
CMD ["redis-server", "/app/redis.conf"]