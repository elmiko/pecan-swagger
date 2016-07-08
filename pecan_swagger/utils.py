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
    swag['consumes'] = []
    swag['produces'] = []
    swag['paths'] = {}
    for p in g.get_paths():
        if p[0] not in swag['paths']:
            swag['paths'][p[0]] = _tuple_to_dict(p[1])
        elif len(p[1]) > 0:
            swag['paths'][p[0]].update(_tuple_to_dict(p[1]))
    return swag


def _tuple_to_dict(tpl):
    """Convert tuple to dictionary
    
    each tuple must have key and value.
    This function arrows taple including lists.

    ex.) acceptable taple
    OK: ('/', ('get',(('desc',{}),('res',{}),('params',['id','name']))))
    NG: ('/', ('get',('desc','res',('params',['id','name']))))
    """
    if isinstance(tpl, list):
        d = []
        for e in tpl:
            d.append(_tuple_to_dict(e))
    elif isinstance(tpl, tuple):
        d = {}
        if isinstance(tpl[0], tuple):
            # tuple has some child tuple
            for e in tpl:
                d[e[0]] = _tuple_to_dict(e[1])
        elif isinstance(tpl[0], list):
            # list member should be processed recursively
            d = _tuple_to_dict(tpl[0])
        else:
            if len(tpl) == 2:
                # single tuple node
                d[tpl[0]] = _tuple_to_dict(tpl[1])
            else:
                raise Exception(tpl)
    else:
        # value or dict
        d = tpl
    return d
