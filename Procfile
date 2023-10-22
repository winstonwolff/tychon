web: cd wasm-as; npx browser-sync start --server --files "./*.html" --files "./*.ty.json" --no-open --no-notify --directory

build_intereter: cd wasm-as; npm run asbuild:watch

compile_tychon: ls wasm-as/main.ty | entr -n python/tychon.py --compile wasm-as/main.ty

