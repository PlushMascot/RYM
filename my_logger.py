def exception_log(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            func_str = func.__name__
            args_str = ', '.join(args)
            kwargs_str = ', '.join([':'.join([str(j) for j in i]) for i in kwargs.items()])
            with open('log.txt', 'w') as f:
                f.write(func_str + '\n')
                f.write(args_str + '\n')
                f.write(kwargs_str + '\n')
            raise
    return wrapper
