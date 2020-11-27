from functools import wraps


# login_required 装饰器
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs, c=1)

    return wrapper


def login_required11(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('c' in kwargs.keys())
        print(*args)
        print(args)
        print(kwargs['c'])
        return func(*args, **kwargs)

    return wrapper


@login_required
@login_required11
def aa(c):
    print(c)


aa()
