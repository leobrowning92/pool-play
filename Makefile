db:
	docker run --rm -it \
	-e POSTGRES_PASSWORD=password \
	-p 5432:5432 postgres:10

setup_tables:
	poetry run python  pool/init_db.py

app: setup_tables
	poetry run python  pool/api/main.py 

test:
	poetry run pytest -vs .