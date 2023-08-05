from collections import namedtuple


class _Xargs(tuple):
    def __repr__(self):
        return f"_Xargs({', '.join(map(repr, self))})"


class _Kwargs(dict):
    def __repr__(self):
        return f"_Kwargs({super().__repr__()})"


_XargsAndKwargs = namedtuple("_XargsAndKwargs", ("xargs", "kwargs"))


class _Constants:
    def __init__(self):
        self.constant_fns = {}

    def __call__(self, *xargs, **kwargs):
        args_ = args(*xargs, **kwargs)
        return self[args_]

    def __getitem__(self, obj):
        if obj not in self.constant_fns:
            def constant(*xargs, **kwargs):
                return obj
            self.constant_fns[obj] = constant
        return self.constant_fns[obj]


def pass_fn():
    "takes no arguments, does nothing"

    pass


def ignore(*xargs, **kwargs):
    "takes arguments (making it slower than pass_fn), does nothing"

    pass


def args(*xargs, **kwargs):
    if xargs:
        if kwargs:
            return _XargsAndKwargs(_Xargs(xargs), _Kwargs(kwargs))
        else:
            if len(xargs) == 1:
                return xargs[0]
            else:
                return _Xargs(xargs)
    else:
        if kwargs:
            return _Kwargs(kwargs)
        else:
            return _Xargs()


constants = _Constants()


def fnn(*xargs):
    """
    fnn stands for “first not-None”. The returned value is the first passed
    argument whose identity is not that of None.
    """

    for arg in xargs:
        if arg is not None:
            return arg

    raise TypeError(f"all passed arguments {xargs} are None")
