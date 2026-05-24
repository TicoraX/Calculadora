import ast
import operator as op

# Diccionario de operaciones permitidas
OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}

def safe_eval(expr, context=None):
    """
    Evalúa una expresión matemática de forma segura usando el AST.
    Solo permite operaciones matemáticas básicas, números y llamadas a funciones
    definidas en el contexto.
    """
    if context is None:
        context = {}

    tree = ast.parse(expr, mode='eval').body

    def _eval(node):
        # Números / constantes
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float, complex)):
                return node.value
            else:
                raise TypeError(f"Constante no permitida: {node.value!r}")
        # Nombres (variables / funciones en el contexto)
        elif isinstance(node, ast.Name):
            if node.id in context:
                return context[node.id]
            else:
                raise NameError(f"Nombre no permitido: '{node.id}'")
        # Operaciones binarias
        elif isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in OPERATORS:
                raise TypeError(f"Operador no permitido: {op_type.__name__}")
            left = _eval(node.left)
            right = _eval(node.right)
            return OPERATORS[op_type](left, right)
        # Operaciones unarias
        elif isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in OPERATORS:
                raise TypeError(f"Operador unario no permitido: {op_type.__name__}")
            operand = _eval(node.operand)
            return OPERATORS[op_type](operand)
        # Llamadas a funciones: solo nombres simples desde el contexto
        elif isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise NameError("Función no permitida: llamadas por atributo no están permitidas")
            func_name = node.func.id
            if func_name not in context:
                raise NameError(f"Función no permitida: '{func_name}'")
            func = context[func_name]
            if not callable(func):
                raise TypeError(f"Objeto no callable en contexto: '{func_name}'")
            if node.keywords:
                raise TypeError("Llamadas con keywords no están permitidas")
            args = [_eval(arg) for arg in node.args]
            return func(*args)
        else:
            raise TypeError(f"Operación no permitida: {type(node).__name__}")

    return _eval(tree)
