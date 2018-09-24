import ast

def execute(code):
    block = ast.parse(code, mode = 'exec')

    last = ast.Expression(block.body.pop().value)

    _globals, _locals = {}, {}
    exec(compile(block, '<string>', mode = 'exec'), _globals, _locals)
    return eval(compile(last, '<string>', mode = 'eval'), _globals, _locals)
