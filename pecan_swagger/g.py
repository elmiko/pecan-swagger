_hierarchy = {}


def add_path(c):
    if _hierarchy.get(c.__swag['name']):
        raise Exception('name {} already exists in hierarchy'.format(c.__swag['name']))
    _hierarchy[c.__swag['name']] = c


def build_path(swaginfo):
    if swaginfo.get('parent') is not None:
        return path_join(build_path(get_swag(swaginfo.get('parent'))),
                         swaginfo.get('endpoint'))
    return swaginfo.get('endpoint')


def get_paths():
    pathlist = []
    for name in _hierarchy:
        fullpath = build_path(get_swag(name))
        methods = methods_get(name)
        ptuple = (fullpath, methods)
        pathlist.append(ptuple)
    return pathlist


def get_swag(name):
    return _hierarchy.get(name).__swag


def methods_get(name):
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
