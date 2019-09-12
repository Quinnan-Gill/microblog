docker run --name microblog -d -p 8000:5000 --rm -e SECRET_KEY=my-secret-key \
    --link mysql:dbserver --link redis:redis-server \
    -e DATABASE_URL=mysql+pymysql://microblog:cow@dbserver/microblog \
    -e REDIS_URL=redis://redis-server:6379/0 \
    microblog:latest