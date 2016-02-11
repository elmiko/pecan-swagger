import pecan_swagger.g as g

"""
decorators module

these decorators are meant to be used by developers who wish to markup
their pecan applications to produce swagger.
"""


def path(endpoint, name, parent=None):
    """
    path decorator

    this decorator should be used on pecan controllers to instruct how
    they map to routes.

    :param endpoint: the root uri for this controller.
    :param name: the name of this path.
    :param parent: an optional path name to indicate a parent/child
                   relationship between this path and another.
    """
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
