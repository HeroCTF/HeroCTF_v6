TARGET=samplehub.tar.xz

all: bundle

bundle:
	rm -rf dist/
	mkdir -p ./dist
	cat .flag.txt \
		| sed -E "s/HERO\{.*\}/HERO\{FAKE_FLAG\}/g" \
		> .flag.temp.txt
	XZ_OPT=-9 tar cJf dist/$(TARGET) \
		--exclude "__pycache__" \
		--transform "s,^,samplehub/," \
		--transform "s,.flag.temp.txt,.flag.txt," \
		--owner=heroctfv6 --group=heroctfv6 --mtime="1970-01-01" \
		src Dockerfile docker-compose.yml .flag.temp.txt
	rm .flag.temp.txt
