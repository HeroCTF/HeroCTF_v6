TARGET=complainio.tar.xz

all: bundle

bundle:
	rm -rf dist/
	mkdir -p ./dist
	cat challenge/flag.txt \
		| sed -E "s/HERO\{.*\}/HERO\{FAKE_FLAG\}/g" \
		> temp_flag.txt
	XZ_OPT=-9 tar cJf dist/$(TARGET) \
                --exclude "flag.txt" \
		--transform "s,^,complainio/," \
		--transform "s,temp_flag.txt,challenge/flag.txt," \
		--owner=heroctfv6 --group=heroctfv6 --mtime="1970-01-01" \
		challenge temp_flag.txt docker-compose.yml
	rm temp_flag.txt
