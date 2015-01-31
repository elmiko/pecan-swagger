_hierarchy = {}


def add_path(c):
    '''adds a named controller to the hierarchy.'''
    if _hierarchy.get(c.__swag['name']):
        raise Exception('name {} already exists in hierarchy'.format(c.__swag['name']))
    _hierarchy[c.__swag['name']] = c


def build_path(swaginfo):
    '''return the route path for a swag metadata item.'''
    if swaginfo.get('parent') is not None:
        return path_join(build_path(get_swag(swaginfo.get('parent'))),
                         swaginfo.get('endpoint'))
    return swaginfo.get('endpoint')


def get_paths():
    '''return all the registered paths

    loops through the hierarchy and retuns a list of tuples containing the
    paths and their methods.

    :returns: [(path, methods), ...]

    '''
    pathlist = []
    for name in _hierarchy:
        fullpath = build_path(get_swag(name))
        methods = methods_get(name)
        ptuple = (fullpath, methods)
        pathlist.append(ptuple)
    return pathlist


def get_swag(name):
    '''return the swag metadata from an named controller.'''
    return _hierarchy.get(name).__swag


def methods_get(name):
    '''get all the methods for a named controller.'''
    c = _hierarchy[name]
    mlist = []
    for i in c.__dict__:
        ii = getattr(c, i)
        if hasattr(ii, '__swag'):
            m = ii.__swag.get('method')
            if m is not None:
                mlist.append(m)
    return mlist


def path_join(part1, part2):
    sep = '/'
    if part1[-1] == sep:
        sep = ''
    return part1 + sep + part2
