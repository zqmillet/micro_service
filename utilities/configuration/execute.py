import ast

from utilities.function_tools import auto_type_checker

@auto_type_checker
def execute(code: str) -> object:
    '''
    this function is used to execute the python code, and get the value of the last line.

    parameters:
        - code:
            this is the python code which will be executed.
    '''

    block = ast.parse(code, mode = 'exec')

    last = ast.Expression(block.body.pop().value)

    _globals, _locals = {}, {}
    exec(compile(block, '<string>', mode = 'exec'), _globals, _locals)
    return eval(compile(last, '<string>', mode = 'eval'), _globals, _locals)
