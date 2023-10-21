'''
Serialize Tychon AST object to JSON so they can be read by WASM interpreter
'''

from _parser import Sym, Call

def dump(astNode):
    if isinstance(astNode, str):
        return f'"{astNode}"'

    elif isinstance(astNode, int):
        return str(astNode)

    elif isinstance(astNode, float):
        return str(astNode)

    elif isinstance(astNode, Sym):
        return f'["Symbol", "{astNode.name}"]'

    elif isinstance(astNode, Call):
        args_json = list(dump(arg) for arg in [astNode.function_name] + astNode.args)
        return f"[{ ', '.join(args_json) }]"


