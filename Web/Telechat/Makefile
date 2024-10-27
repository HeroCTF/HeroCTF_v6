TARGET=telechat.tar.xz

all: bundle

bundle:
	rm -rf dist/
	mkdir -p ./dist
	cat src/run_root.sh \
		| sed -E "s/HERO\{.*\}/HERO\{FAKE_FLAG\}/g" \
		> temp_run_root.sh
	XZ_OPT=-9 tar cJf dist/$(TARGET) \
                --exclude "run_root.sh" \
		--transform "s,^,telechat/," \
		--transform "s,temp_run_root.sh,src/run_root.sh," \
		--owner=heroctfv6 --group=heroctfv6 --mtime="1970-01-01" \
		src temp_run_root.sh README_players.md
	rm temp_run_root.sh
