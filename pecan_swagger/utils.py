import json

from pecan_swagger import g as g


def swagger_build(title, version):
    swag = dict(swagger='2.0',
                info=dict(title=title, version=version),
                paths={})
    for p in g.get_paths():
        swag['paths'][p[0]] = {k: {} for k in p[1]}
    return json.dumps(swag, indent=2)
