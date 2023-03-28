
.PHONY: web
web:
	open -a FireFox "http://localhost:8000" && python3 -m http.server

.PHONY: watch
watch:
	while true; do make --silent build; sleep .5; done

build: pkg/webasm.js index.html

pkg/webasm.js: src/*.rs
	wasm-pack build --target web

clean:
	mv target ~/.Trash
	mv pkg ~/.Trash

