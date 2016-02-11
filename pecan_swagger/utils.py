from pecan_swagger import g as g


"""
utility function module

this module contains the utility functions to assemble the swagger
dictionary object. they can be consumed by end-user applications to
build up swagger objects for applications.

functions:
swagger_build -- build a full swagger dictionary
"""


def swagger_build(title, version):
    swag = dict()
    swag['swagger'] = '2.0'
    swag['info'] = dict(title=title, version=version)
    swag['paths'] = {}
    for p in g.get_paths():
        if len(p[1]) > 0:
            swag['paths'][p[0]] = {k: {} for k in p[1]}
    return swag
