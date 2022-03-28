db:
	docker run --rm -it \
	-e POSTGRES_PASSWORD=password \
	-p 5432:5432 postgres:10