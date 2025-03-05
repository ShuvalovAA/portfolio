# Основное

обновление через helm - helm upgrade rr-email-sender ./helm -n rr-email-sender -f ./helm/values.staging.yaml --
	config=PATH_TO_STAGE_CONFIG
	поставить поды - helm install rr-email-sender ./helm -n rr-email-sender -f ./helm/values.staging.yaml
	убить поды - helm uninstall rr-email-sender -n rr-email-sender
	helm install changeset ./helm -n changeset -f ./helm/values.staging.yaml
	kubectl create namespace changeset