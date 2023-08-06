import inspect


def get_call_info(self):
    _stack = inspect.stack()[1]
    cls = _stack[0].f_locals['self'].__class__
    cls_name = cls.__name__
    fnc = _stack[3]
    return (cls, cls_name, fnc)
