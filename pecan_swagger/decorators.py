import pecan_swagger.g as g

def path(endpoint, name, parent=None):
    def decorator(c):
        if hasattr(c, '__swag'):
            raise Exception('{} already has swag'.format(c.__name__))
        c.__swag = dict(endpoint=endpoint, name=name, parent=parent)
        g.add_path(c)
        return c
    return decorator

def method(method):
    def decorator(m):
        if hasattr(m, '__swag'):
            raise Exception('{} already has swag'.format(m.__name__))
        m.__swag = dict(method=method)
        return m
    return decorator
