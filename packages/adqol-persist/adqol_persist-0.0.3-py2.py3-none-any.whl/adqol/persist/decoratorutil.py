import ast, inspect, operator
import logging

from adqol.persist.fielduse import FieldUse

"""
@decorator
def field(func, *args, **kw): 
    result = func(*args, **kw)
    return result
"""

def flatten_attr(node):
    if isinstance(node, ast.Attribute):
        return str(flatten_attr(node.value)) + '.' + node.attr
    elif isinstance(node, ast.Name):
        return str(node.id)
    else:
        pass

_binOps = {
    ast.BitAnd: operator.iand,
    ast.BitOr: operator.ior
}

def _eval(node):
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    elif isinstance(node, ast.Str):
        return node.s
    elif isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.Name):
        return str(node.id)
    elif isinstance(node, ast.Attribute):
        return eval(_eval(node.value) + '.' + node.attr + '.value')
    elif isinstance(node, ast.BinOp):
        try:
            return _binOps[type(node.op)](_eval(node.left), _eval(node.right))
        except:
            return "-1"
    else:
        raise Exception('Unsupported type {}'.format(node))
    return _eval(node.body)


def getEntityInfos(target, decname):
    res = {}

    def visit_ClassDef(node):
        for e in node.decorator_list:
            if not ((isinstance(e, ast.Call) and _eval(e.func) == str(decname)) or (isinstance(e, ast.Name) and _eval(e) == str(decname))):
                continue

            if isinstance(e, ast.Call) and _eval(e.func) == str(decname):
                for kw in e.keywords:
                    if kw.arg == 'table':
                        res['table']=_eval(kw.value)
    
    V = ast.NodeVisitor()
    V.visit_ClassDef = visit_ClassDef
    V.visit(compile(inspect.getsource(target), '?', 'exec', ast.PyCF_ONLY_AST))
    return res

def getFieldInfos(target, decname):
    res = {'fields': {}, 'keys': []}

    def visit_FunctionDef(node):
        for e in node.decorator_list:
            if not ((isinstance(e, ast.Call) and flatten_attr(e.func) == str(decname)) or (isinstance(e, ast.Name) and flatten_attr(e) == str(decname))):
                continue
    
            res['fields'][node.name] = {'uses': FieldUse.ALL.value }
            
            if isinstance(e, ast.Call) and flatten_attr(e.func) == str(decname):
                for kw in e.keywords:
                    if kw.arg == 'name' or kw.arg == 'uses':
                        res['fields'][node.name][kw.arg]=_eval(kw.value)
                    if kw.arg == 'key':
                        res['keys'].append(kw.value.s)
    
    V = ast.NodeVisitor()
    V.visit_FunctionDef = visit_FunctionDef
    V.visit(compile(inspect.getsource(target), '?', 'exec', ast.PyCF_ONLY_AST))
    return res
