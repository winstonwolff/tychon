BUILD_DIR = build

.PHONY: run-node
run-node: build
	echo "\n\n--- running ---\n"
	cd $(BUILD_DIR); node hello.js

.PHONY: build

build:
	echo "build dir="
	echo $(BUILD_DIR)
	emcc hello.c -o $(BUILD_DIR)/hello.html

brew: .brew-installed.txt

.brew-installed.txt:
	brew install bdw-gc
	echo "brew installed ${date}" > .brew-installed.txt


web:
	cd $(BUILD_DIR); python3 -mhttp.server

.PHONY: clean
clean:
	rm -rf $(BUILD_DIR)/*
