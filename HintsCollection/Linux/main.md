# Основное

## Ubuntu >=22.04

посмотреть зомби процессы ps aux | grep 'Z'
	экспорт переменных из файла - export $(cat .env | xargs)
	поиск файлов содержащих текст - ack "1\.1\.1"
	настройка визуализации баш - ~/.bashrc


## supervisord
	логи - cat  /var/log/supervisor/supervisord.log | grep 'stop' | tail -1000

## awk
отоброзить конкретные столбцы - awk '{print $1,$3}'

## sort
	сортировать по 3 столбцу - |sort -nk 3


посмотреть загрузку по памяти на каждый процесс 
	sudo supervisorctl status | awk '{print $4}' | grep -o '[0-9]\+'
	логи процесса -  sudo supervisorctl tail -100 zagruzka_callbacks:00 
	использование cpu процессоров - ps aux --sort=-"%cpu" | head
	самые прожорливые процессы воркеров по RSS - ps ax -o %mem,rss,%cpu,pid,cmd | sort -nk 2 -r | head | awk 'NR>0 {$2=int($2/1024)"M";}{ print;}'
	- watch 'ps ax -o %mem,rss,%cpu,pid,cmd | sort -nk 2 | tail '
	
	
	for number in $(sudo supervisorctl status | awk '{print $1}' | grep -o '[a-Z]\+') ; do echo $(ps ax -o %mem,rss,%cpu,pid,cmd | sort -nk 2 | tail | awk 'NR>1 {$2=int($2/1024)"M";}{ print;}' | grep $number); done