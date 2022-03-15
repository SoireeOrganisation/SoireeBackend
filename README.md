# soireeBackend
Данный репозиторий содержит исходные файлы бэкенда проекта.
## Лендинг проекта
http://soiree-app.tilda.ws

## Инстркуция по сборке и запуску
```shell
sudo docker pull bopobywek/soiree:latest
sudo docker pull postgres:13-alpine
sudo docker run --restart=always --name psql -d -e POSTGRES_USER=soiree_admin \
  -e POSTGRES_PASSWORD=123abc -e POSTGRES_DB=soiree postgres:13-alpine
sudo docker run --restart=always --name web -d -p 80:80 \
 --link psql:db -e DATABASE_URL=postgresql://soiree_admin:123abc@db:5432/soiree \
  -e MAIL_USERNAME="soiree.app@list.ru" -e MAIL_PASSWORD=TrmNDR2ASidLGCC4R92i \
   bopobywek/soiree:latest
```
