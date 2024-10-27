TARGET=under-construction.tar.xz

all: bundle

bundle:
	rm -rf dist/
	mkdir -p ./dist
	cat docker-compose.yml \
		| sed -E "s/FLAG=.*/FLAG=HERO\{FAKE_FLAG\}/g" \
		> docker-compose.temp.yml
	XZ_OPT=-9 tar cJf dist/$(TARGET) \
		--exclude "__pycache__" \
		--transform "s,^,under-construction/," \
		--transform "s,docker-compose.temp.yml,docker-compose.yml," \
		--owner=heroctfv6 --group=heroctfv6 --mtime="1970-01-01" \
		src docker-compose.temp.yml
	rm docker-compose.temp.yml
