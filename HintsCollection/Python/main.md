# Основное

## чистка кода
	flake8
	mypy
	black --skip-string-normalization --line-length 79 --fast


python3 -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt
	pip install --index-url https://my.local.mirror.com/simple -r requirements.txt
	импровизация shell для проекта - export PYTHONPATH="./src:$PYTHONPATH" && pip install -r requirements.py && python(переменные окружения подтянуть отдельно