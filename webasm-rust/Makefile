# Makefile

.PHONY: web
web:
	open -a FireFox "http://localhost:8000" && python3 -m http.server

.PHONY: watch
watch:
	ls *.* rust/src/* | entr make build

build: pkg/webasm.js index.html

pkg/webasm.js: rust/src/*.rs
	cd rust; wasm-pack build --target web

clean:
	rm -rf rust/target
	rm -rf rust/pkg

