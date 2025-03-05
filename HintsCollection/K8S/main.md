# Основное
kubectl -n users rollout restart deployment users - рестартнуть по деплойменту конкретный под
	----   kubectl run wget --image=busybox:1.28 --rm --it --restart=Never \
	--command -- wget -qO- http://demo:8888
	----   kubectl run demo --image cloudnatived/demo:hello --expose --port 8888
	----   Отладка в режиме реального времени
	с помощью kubesquash
	посмотрет поды по конфигу - kubectl --kubeconfig=staging_config -n dev-skazka get pods -A
	проволиться в конкретный под - kubectl --kubeconfig=staging_config -n dev-skazka exec -itt skazka-django-backend-758789b4b-fgt6b bash
	рестарт пода - kubectl --kubeconfig=staging_config -n dev-skazka rollout restart deployment skazka-celery-workers-common
	обновление фронта -  kubectl --kubeconfig=staging_config -n dev-skazka rollout restart deployment skazka-vue-frontend и под джанги
	kubectl(вызов утилиты) create deployment(команда) first-deployment(имя пода)  --image=ksxack/lesson1:v0.2(какой образ имя_пользователя_докера/образ) - императивно
	kubectl apply -f deployment.yaml - декларативно
	get, create, edit - императивно
	apply - декларативно
	kubectl rollout history deployment/goapp-deployment     # Проверить историю деплоймента
	kubectl rollout undo deployment/goapp-deployment        # Откатиться к предыдущей версии деплоймента
	kubectl rollout restart deployment/goapp-deployment     # Плавающий рестарт Подов в деплойменте 
	kubectl config get-contexts                          # показать список контекстов
	kubectl config current-context                       # показать текущий контекст (current-context)
	kubectl config use-context my-cluster-name           # установить my-cluster-name как контекст по умолчанию
	kubectl apply -f ./my-manifest.yaml            # создать объект из файла
	kubectl create deployment nginx --image=nginx  # запустить один экземпляр nginx
	kubectl get pods -o wide                      # Вывести все поды и показать, на каких они нодах
	kubectl describe pods my-pod                  # Просмотреть 
	ормацию о поде такую как # старта, количество и причины рестартов, QoS-класс и прочее
	kubectl logs -f my-pod                        # Просмотр логов в режиме реального времени
	kubectl top pods                              # Вывести информацию об утилизации ресурсов подами
	kubectl edit pod my-pod                       # Изменение .yaml манифеста пода
	kubectl delete pod my-pod                       # Удаление пода или kubectl delete deployment 
	kubectl exec -it -n namespace-name podname sh   # На конце выбираем оболочку, если нет sh, ставим bash
	kubectl cp {{namespace}}/{{podname}}:path/to/directory /local/path  # Копирование файла из Пода
	kubectl cp /local/path namespace/podname:path/to/directory          # Копирования файла в Под
	kubectl port-forward pods/mongo-75f59d57f4-4nd6q 28015:27017  # Проброс порта Пода
	kubectl port-forward mongo-75f59d57f4-4nd6q 28015:27017       # Проброс порта Сервиса
	пробросить порт - kubectl port-forward  -n lesson14(имя неймспейса) static-web(имя пода) 8080:8080
	переключение между кластерами - kubectl config use-context <minikube> or kubectx
	kubectl -n rr-email-sender  exec -it rr-email-sender-57b9596d58-4m6k2 -- env - посмотреть переменные окружения пода
	kubectl -n users get pods -w - смотреть раскатку
	kubectl -n dev-skazka scale deployments/<название развёртывания> --replicas=<количество реплик> - изменить количество реплик пода
	

# СПРАВКА
## контроллеры
    DaemonSet - поддерживает по одной реплике Пода на каждой из Нод кластера
    Job - Джоба поднимает под, отрабатывает и помирает до следующего запуска
    CronJob - джоба должна запускаться по расписанию, используйте механизм