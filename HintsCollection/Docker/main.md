# Основное

интерактивная работа с портом
docker-compose run --rm --service-ports ${MY_CONTAINER}
старт докера
sudo service docker start
список сервисов
docker-compose config --service
авторизоваться docker login
выложить образ docker tag go:v0.2 shuvalovartal/lesson1:v0.2 - добавить тэг
закинуть образ docker push <Ваш username в Докерхаб>/lesson1:v0.2
docker attach skazka-skazka-1
очистить docker - docker system prune -f


/etc/docker/daemon.json
{
  "live-restore": true,
  "log-driver": "json-file",
  "log-opts": { "max-size": "256m" },
  "dns": [
    "10.216.136.108",
    "10.216.140.76",
    "8.8.8.8",
    "1.1.1.1"
  ],
  "dns-opts": [
    "timeout:1",
    "attempts:2"
  ],
  "features": {
    "buildkit": true
  }
}