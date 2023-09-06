BUILD_DIR = build

.PHONY: run-node
run-node: $(BUILD_DIR)/hello.wasm
	cd $(BUILD_DIR); node hello.js

# INC_FLAGS = "-I/opt/homebrew/include"
# LINK_FLAGS = "-L/opt/homebrew/lib/libgc.a"
$(BUILD_DIR)/hello.wasm: hello.c makefile
	emcc hello.c lib/hamt/hamt.c -o $(BUILD_DIR)/hello.html $(INC_FLAGS)
	@echo "--- COMPILE DONE ---\n"

brew: .brew-installed.txt

.brew-installed.txt:
	brew install bdw-gc
	echo "brew installed ${date}" > .brew-installed.txt


web:
	cd $(BUILD_DIR); python3 -mhttp.server

.PHONY: clean
clean:
	rm -rf $(BUILD_DIR)/*

