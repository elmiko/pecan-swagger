import collections
import json

from pecan_swagger import g as g


def swagger_build(title, version):
    swag = collections.OrderedDict()
    swag['swagger']='2.0'
    swag['info']=dict(title=title, version=version)
    swag['paths']={}
    for p in g.get_paths():
        if len(p[1]) > 0:
            swag['paths'][p[0]] = {k: {} for k in p[1]}
    return json.dumps(swag, indent=2)
