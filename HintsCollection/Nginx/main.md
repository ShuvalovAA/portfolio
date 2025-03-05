# Основное

sudo mcedit /etc/nginx/sites-enabled/upstreams - редактировать upstream
	sudo nginx -t - проверить синтаксис upstream
	sudo nginx -s reload - релоад сервера с сохранением сессий
	или sudo vim /etc/nginx/common/upstream.conf && sudo /etc/init.d/nginx configtest && sudo /etc/init.d/nginx reload
	запуск джобы отдельного бэка через передачу key EXTRA_ARGS и -l  skazka-backend-0{номер бэка}