web: cd wasm-as; npx browser-sync start --server --files "./*" --no-open --no-notify

build_intereter: cd wasm-as; npm run asbuild:watch

compile_tychon: ls wasm-as/main.ty | entr -n python/tychon.py --compile wasm-as/main.ty

