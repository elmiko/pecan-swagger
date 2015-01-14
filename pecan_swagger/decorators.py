import pecan_swagger.g as g

def path(endpoint, name, parent=None):
    def classwrap(c):
        if hasattr(c, '__swag'):
            raise Exception('class {} already has swag'.format(c.__name__))
        c.__swag = dict(endpoint=endpoint, name=name, parent=parent)
        g.add_path(c)
        return c
    return classwrap
