# Makefile

.PHONY: web
web:
	open -a FireFox "http://localhost:8000" && python3 -m http.server

.PHONY: watch
watch:
	ls *.* src/* | entr make build

build: pkg/webasm.js index.html

pkg/webasm.js: src/*.rs
	wasm-pack build --target web

clean:
	mv target ~/.Trash
	mv pkg ~/.Trash

