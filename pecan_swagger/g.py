import copy
import inspect

from pecan import util as p_u
import six


"""
global hierarchy module

this module is at the heart of the swagger conversion utility. it
contains a global "hierarchy" object which will provide a single point
to assemble an application's swagger output.

there are also several helper functions to assist in building the
hierarchy of controllers, routes, and methods.
"""

_hierarchy = {}

_http_methods = {'GET': '', 'POST': '', 'PUT': '',
                 'PATCH': '<specifier>', 'DELETE': '<specifier>',
                 'HEAD': '', 'TRACE': ''}

def add_path(c):
    """adds a named controller to the hierarchy."""
    if _hierarchy.get(c.__swag['name']):
        raise Exception(
            'name {} already exists in hierarchy'.format(c.__swag['name']))
    _hierarchy[c.__swag['name']] = c


def build_path(swaginfo):
    """return the route path for a swag metadata item."""
    if swaginfo.get('parent') is not None:
        return path_join(build_path(get_swag(swaginfo.get('parent'))),
                         swaginfo.get('endpoint'))
    return swaginfo.get('endpoint')


def get_controller_paths(controllers):
    """
    get a list of paths with methods

    returns a list of tuples (controller path, methods).
    """
    def get_methods_for_generic(name):
        methods = []
        generic_handlers = lc.get(name).get('generic_handlers', {})
        for method, func in generic_handlers.items():
            if method == 'DEFAULT':
                methods.append('GET')
            else:
                methods.append(method)
            # TODO drill down through decorators to get true function name
            truename = getrealname(func)
            del lc[truename]
        return methods

    def append_methods_for_specific(name, tpl):
        paths.append(tpl)
        del lc[name]

    lc = copy.deepcopy(controllers)
    paths = []
    # TODO incorporate method decorator, removing functions marked
    if lc.get('index'):
        paths.append(('', get_methods_for_generic('index')))

    # for REST controller
    for method, path in _http_methods.items():
        func = method.lower()
        if lc.get(func):
            append_methods_for_specific(func, (path, [method]))

    if lc.get('get_all'):
        append_methods_for_specific('get_all', ('', ['GET']))
    if lc.get('get_one'):
        append_methods_for_specific('get_one', ('<specifier>', ['GET']))

    if lc.get('_default'):
        append_methods_for_specific('_default', ('<default>', ['*']))
    if lc.get('_route'):
        append_methods_for_specific('_route', ('<route>', ['*']))
    if lc.get('_lookup'):
        del lc['_lookup']

    if lc.get('_custom_actions'):
        for ca, ca_method in lc['_custom_actions'].items():
            paths.append((ca, ca_method))
        del lc['_custom_actions']

    generic_controllers = [c for c in lc if lc[c].get('generic')]
    for controller in generic_controllers:
        paths.append((controller, get_methods_for_generic(controller)))
    for controller in lc:
        if controller not in [path[0] for path in paths]:
            paths.append((controller, ['GET']))
    return paths


def get_controllers(name):
    """
    get all the controllers associated with a path

    returns a dictionary of controllers indexed by their names.
    """
    c = _hierarchy[name]
    controllers = {k: p_u._cfg(v)
                   for k, v in c.__dict__.items() if p_u.iscontroller(v)}
    cacts = {k: v for k, v in c.__dict__.items() if k == '_custom_actions'}
    if len(cacts):
        controllers.update(cacts)
    return controllers

def get_paths():
    """
    return all the registered paths

    loops through the hierarchy and retuns a list of tuples containing the
    paths and their methods.

    :returns: [(path, methods), ...]
    """
    pathlist = []
    for name in _hierarchy:
        fullpath = build_path(get_swag(name))
        controllers = get_controllers(name)
        paths = get_controller_paths(controllers)
        for path in paths:
            ptuple = (path_join(fullpath, path[0]), path[1])
            pathlist.append(ptuple)
    return pathlist


def get_swag(name):
    """return the swag metadata from an named controller."""
    return _hierarchy.get(name).__swag


def getrealname(method):
    """attempt to get a method's real name."""
    argspec = inspect.getargspec(method)
    args = argspec[0]
    if args and args[0] == 'self':
        return method.__name__
    if hasattr(method, '__func__'):
        method = method.__func__

    func_closure = six.get_function_closure(method)

    # NOTE(sileht): if the closure is None we cannot look deeper,
    # so return actual argspec, this occurs when the method
    # is static for example.
    if func_closure is None:
        return method.__name__

    closure = next(
        (
            c for c in func_closure if six.callable(c.cell_contents)
        ),
        None
    )
    method = closure.cell_contents
    return getrealname(method)


def methods_get(name):
    """get all the methods for a named controller."""
    c = _hierarchy[name]
    mlist = []
    if hasattr(c, 'index') and p_u.iscontroller(c.index):
        cfg = p_u._cfg(c.index)
        if cfg.get('generic_handlers').get('DEFAULT'):
            mlist.append('GET')
        mlist += cfg.get('allowed_methods')
    for i in c.__dict__:
        ii = getattr(c, i)
        if hasattr(ii, '__swag'):
            m = ii.__swag.get('method')
            if m is not None:
                mlist.append(m)
    return mlist


def path_join(part1, part2):
    """join two url paths."""
    if len(part2) == 0:
        return part1
    sep = '/'
    if part1[-1] == sep:
        sep = ''
    return part1 + sep + part2
