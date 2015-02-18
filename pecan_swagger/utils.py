import collections

from pecan_swagger import g as g


def swagger_build(title, version):
    swag = dict()
    swag['swagger']='2.0'
    swag['info']=dict(title=title, version=version)
    swag['paths']={}
    for p in g.get_paths():
        if len(p[1]) > 0:
            swag['paths'][p[0]] = {k: {} for k in p[1]}
    return swag

def controllers_build():
    ctlrs = {}
    for p in g.get_paths():
        ctlrs[p[0]] = p[2]
    return ctlrs

def paths_build():
    paths = {}
    for p in g.get_paths():
        paths[p[0]] = p[3]
    return paths
