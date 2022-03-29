db:
	docker run --rm -it \
	-e POSTGRES_PASSWORD=password \
	-p 5432:5432 postgres:10


app:
	poetry run python  pool/api/main.py

test:
	poetry run pytest .