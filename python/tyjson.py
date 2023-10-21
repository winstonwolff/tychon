'''
Serialize Tychon AST object to JSON so they can be read by WASM interpreter
'''

import json
from _parser import Sym, Call
from pprint import pformat

def dump(ast_graph, pretty=False):
    if pretty:
        return pformat(nodeAsJson(ast_graph), indent=4, width=120)
    else:
        return json.dumps(nodeAsJson(ast_graph)) + "\n"



def nodeAsJson(ast_node):
    if isinstance(ast_node, (str, int, float)):
        return ast_node

    elif isinstance(ast_node, Sym):
        return ["Symbol", ast_node.name]

    elif isinstance(ast_node, Call):
        return [ast_node.function_name] + [nodeAsJson(arg) for arg in ast_node.args]

    elif isinstance(ast_node, (list, tuple)):
        return [nodeAsJson(part) for part in ast_node]

    elif ast_node is None:
        return ""

    raise Exception(f'Unknown node: { repr(ast_node) }')

