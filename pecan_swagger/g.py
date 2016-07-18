import copy
import inspect

from pecan import util as p_u
import wsme.types as wtypes
import six
import weakref


"""
global hierarchy module

this module is at the heart of the swagger conversion utility. it
contains a global "hierarchy" object which will provide a single point
to assemble an application's swagger output.

there are also several helper functions to assist in building the
hierarchy of controllers, routes, and methods.
"""

_hierarchy = {}

_http_methods = {'get': '', 'post': '', 'put': '',
                 'patch': '<specifier>', 'delete': '<specifier>',
                 'head': '', 'trace': ''}

_all_wsme_types = wtypes.native_types + (
    wtypes.ArrayType, wtypes.DictType, wtypes.BinaryType,
    wtypes.IntegerType, wtypes.StringType, wtypes.IPv4AddressType,
    wtypes.IPv6AddressType, wtypes.UuidType, wtypes.Enum, wtypes.UnsetType)


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


def get_controller_paths(controllers, wsme_defs):
    """
    get a list of paths with methods

    returns a list of tuples (controller path, methods).
    """
    def get_methods_for_generic(name):
        methods = []
        generic_handlers = lc.get(name).get('generic_handlers', {})
        for method, func in generic_handlers.items():
            if method == 'DEFAULT':
                methods.append('get')
            else:
                methods.append(method.lower())
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
        for method in get_methods_for_generic('index'):
            paths.append(('', (method, {})))

    # for REST controller
    for method, path in _http_methods.items():
        if lc.get(method):
            spec = wsme_defs.get(method, {})  # add wsme definitions
            append_methods_for_specific(method, (path, (method, spec)))

    if lc.get('get_all'):
        # add wsme definitions
        spec = wsme_defs.get('get_all')  # add wsme definitions
        append_methods_for_specific('get_all', ('', ('get', spec)))
    if lc.get('get_one'):
        # add wsme definitions
        spec = wsme_defs.get('get_one')  # add wsme definitions
        append_methods_for_specific('get_one', ('<specifier>', ('get', spec)))

    if lc.get('_default'):
        append_methods_for_specific('_default', ('<default>', ('*', {})))
    if lc.get('_route'):
        append_methods_for_specific('_route', ('<route>', ('*', {})))
    if lc.get('_lookup'):
        del lc['_lookup']

    if lc.get('_custom_actions'):
        for ca, ca_method in lc['_custom_actions'].items():
            spec = wsme_defs.get(ca)  # add wsme definitions
            for m in ca_method:
                paths.append((ca, (m.lower(), spec)))
        del lc['_custom_actions']

    generic_controllers = [c for c in lc if lc[c].get('generic')]
    for controller in generic_controllers:
        for method in get_methods_for_generic(controller):
            paths.append((controller, (method, {})))
    for controller in lc:
        if controller not in [path[0] for path in paths]:
            paths.append((controller, ('get', {})))
    return paths


def get_wsme_defs(name):

    def datatype_to_type_and_format(datatype):
        tf = {}
        if datatype == 'uuid' or datatype == 'ipv4address' \
                or datatype == 'ipv6address' or datatype == 'date' \
                or datatype == 'time':
            tf['type'] = 'string'
            tf['format'] = datatype
        elif datatype == 'datetime':
            tf['type'] = 'string'
            tf['format'] = 'date-time'
        elif datatype == 'binary' or datatype == 'bytes':
            # base64 encoded characters
            tf['type'] = 'string'
            tf['format'] = 'byte'
        elif datatype == 'array' or datatype == 'boolean' \
                or datatype == 'integer' or datatype == 'string':
            # no format
            tf['type'] = datatype
        elif datatype == 'float':
            # number
            tf['type'] = 'number'
            tf['format'] = datatype
        elif datatype == 'unicode' or datatype == 'str' \
                or datatype == 'text':
            # primitive, no format
            tf['type'] = 'string'
        elif datatype == 'int' or datatype == 'decimal':
            # primitive, no format
            tf['type'] = 'integer'
        elif datatype == 'bool':
            # primitive, no format
            tf['type'] = 'boolean'
        elif datatype == 'enum':
            tf['type'] = 'enum'
        elif datatype == 'unset' or datatype == 'none':
            tf['type'] = None
        elif datatype == 'dict':
            tf['type'] = 'object'
        else:
            tf['type'] = 'object'
        return tf

    def class_to_name_str(c):
        return (('%s' % c).replace('<', '').replace('>', '')
                .replace('class ', '').replace('\'', '')
                .split(' ', 1)[0].rsplit('.', 1)[-1])

    def conv_class_name_to_type_str(cn):
        type_str = ''
        if cn.endswith('Type'):
            type_str = cn[:-4]
        elif cn == 'str':
            type_str = 'string'
        else:
            type_str = cn
        type_str = type_str.lower()
        return type_str

    def get_type_str(obj, src_dict=None):
        type_str = ''
        if hasattr(obj, '__name__'):
            type_str = obj.__name__
        else:
            type_str = obj.__class__.__name__
        type_str = conv_class_name_to_type_str(type_str)

        tf = datatype_to_type_and_format(type_str)

        if hasattr(obj, 'basetype') and \
                (obj.__class__ not in _all_wsme_types or type_str == 'enum'):
            # UserType or Enum
            tf['type'] = get_type_str(obj.basetype)

        if isinstance(src_dict, dict):
            # if dict is in args, set 'type' and 'format' into the dict and
            # return
            src_dict.update({'type': tf['type']})
            if 'format' in tf:
                src_dict.update({'format': tf['format']})

            # get datatype options. ex.) min_length, minimum, ..
            for k, v in inspect.getmembers(obj):
                if ((k == 'minimum' or k == 'maxmum'
                        or k == 'min_length' or k == 'max_length')
                        and v is not None):
                    src_dict[to_swag_key(k)] = v
                elif k == 'pattern' and v is not None:
                    src_dict[to_swag_key(k)] = v.pattern
                # TODO(shu-mutou): this should be removed for production.
                # else:
                #     src_dict[to_swag_key(k)] = v

            if type_str == 'enum':
                # EnumType use 'set' that doesn't have sequence.
                # So use 'sorted' for keeping static output.
                src_dict['enum'] = sorted([v for v in obj.values])

        # return 'type' only
        return tf['type']

    def to_swag_key(key):
        keys = {
            'doc': 'description',
            'arguments': 'parameters',
            'return_type': 'schema',
            'datatype': 'type',
            'mandatory': 'required',
            'sample': 'examples',
            'readonly': 'readOnly',
            'min_length': 'minLength',
            'max_length': 'maxLength',
        }
        if key in keys:
            return keys[key]
        else:
            return key

    def get_wm_item_prop(item, isparams=False):
        # Add prop into 'properties' and 'required' in 'Items Object'
        # 'Items Object' can be part of 'Schema Object' or 'Items Object',
        # and can use recursively
        prop_dict = {}
        # TODO(shu-mutou): this should be removed for production.
        # prop_dict['obj'] = inspect.getmembers(item)

        _item = item
        if wtypes.iscomplex(item):
            _item = weakref.ref(item)

        for a, i in inspect.getmembers(_item):
            if a == 'datatype':
                datatype = get_type_str(i, prop_dict)
                if datatype == 'array':
                    # if array, do recursively
                    prop_dict['items'] = inspect_wm_schema(i.item_type)
                elif datatype == 'object':
                    # if obuject, do recursively
                    prop_dict['items'] = inspect_wm_schema(i)
            elif a == 'default' and i:
                    prop_dict[to_swag_key(a)] = i
            elif a == 'name' and isparams:
                prop_dict[to_swag_key(a)] = i
            elif a == 'mandatory' and i:
                prop_dict[to_swag_key(a)] = i
            elif a == 'readonly' and i:
                prop_dict[to_swag_key(a)] = i
            elif a == 'doc' and i is not None:
                prop_dict[to_swag_key(a)] = i

        if isparams and prop_dict['type'] in ['object', 'array']:
            prop_dict['schema'] = {'items': prop_dict['items'],
                                   'type': prop_dict['type']}
            del prop_dict['type']
            del prop_dict['items']
        return prop_dict

    def get_wsattr_and_wsproperty(obj):
        ws_dict = {}
        for key, value in inspect.getmembers(obj):
            if (key[0] != '_' and
                    (value.__class__.__name__ == 'wsattr'
                     or value.__class__.__name__ == 'wsproperty')):
                ws_dict[key] = value
        return ws_dict

    def inspect_wm_schema(schema_obj, isparams=False):
        schema_dict = {}
        # TODO(shu-mutou): this should be removed for production.
        # schema_dict['obj'] = get_wsattr_and_wsproperty(schema_obj)
        ws_len = len(get_wsattr_and_wsproperty(schema_obj))
        for key, obj in inspect.getmembers(schema_obj):
            if (key[0] != '_' and
                    (obj.__class__.__name__ == 'wsattr'
                     or obj.__class__.__name__ == 'wsproperty')):
                # TODO(shu-mutou): this should be removed for production.
                # schema_dict[to_swag_key(key)] = \
                #     {'obj': inspect.getmembers(obj)}

                if ws_len == 1:
                    # single schema
                    schema_dict = get_wm_item_prop(obj, isparams)
                else:
                    # multi property schema
                    schema_dict.update({'type': 'object'})
                    # properties
                    if 'items' not in schema_dict:
                        schema_dict['items'] = {'properties': {}}
                    prop = {key: get_wm_item_prop(obj, isparams)}
                    # required as array of string
                    if 'required' in prop[key] and prop[key]['required'] \
                       and isinstance(prop[key]['required'], bool):
                        if 'required' not in schema_dict:
                            schema_dict['required'] = []
                        schema_dict['required'].append(key)
                        del prop[key]['required']
                    schema_dict['items']['properties'].update(prop)
        return schema_dict

    def get_wm_def(o):
        wsme = {'description': ''}
        for w, d in inspect.getmembers(o):
            if w == 'arguments':
                wsme[to_swag_key(w)] = []
                for arg in d:
                    # set each 'Parameter Object', it can include
                    # 'Items Object' recursively
                    item_dict = get_wm_item_prop(arg, True)
                    # TODO: MUST be set one of
                    # 'body|query|path|header|formData'
                    item_dict['in'] = 'query'
                    wsme[to_swag_key(w)].append(item_dict)
                # 'body' should be set due to existing 'body' option
                # in WSME expose
                if o.body_type is not None:
                    # if body is set, last arg is it.
                    wsme[to_swag_key(w)][-1]['in'] = 'body'
            elif w == 'doc' and d:
                wsme[to_swag_key(w)] = d
            elif w == 'return_type':
                wsme['responses'] = {'status': {'description': ''}}
                if d:
                    if d in _all_wsme_types:
                        # d is set single WSME type class or implicit type
                        wsme['responses']['status'][to_swag_key(w)] = (
                            datatype_to_type_and_format(
                             conv_class_name_to_type_str(
                              class_to_name_str(d))))
                    else:
                        # d is model class
                        wsme['responses']['status'][to_swag_key(w)] = (
                            inspect_wm_schema(d, False))
                    doc = inspect.getdoc(d)
                    if doc is not None:
                        wsme['responses']['status']['description'] = doc
            elif w == 'status_code':
                wsme['responses'][d] = \
                    copy.deepcopy(wsme['responses']['status'])
                del wsme['responses']['status']
            # TODO(shu-mutou): this should be removed for production.
            # elif w == 'body_type':
            #     wsme[to_swag_key(w)] = get_type_str(d)
            # elif w == 'extra_options' or w == 'ignore_extra_args' \
            #      or w == 'name' or w == 'pass_request':
            #     wsme[to_swag_key(w)] = d
            # else:
            #     wsme[to_swag_key(w)] = d
        return wsme

    c = _hierarchy[name]
    wsme_defs = {}
    for k, v in inspect.getmembers(c):
        if p_u.iscontroller(v):
            for m, o in inspect.getmembers(v):
                if m == "_wsme_definition":
                    wsme_defs[k] = get_wm_def(o)

    # TODO(shu-mutou): this should be removed for production.
    # output wsme info into files by each controller for dev
    # import pprint
    # with open(name + '.txt', 'w') as fout:
    #     pprint.pprint(wsme_defs, stream=fout, indent=2)

    return wsme_defs


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
        wsme_defs = get_wsme_defs(name)
        paths = get_controller_paths(controllers, wsme_defs)
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
            mlist.append('get')
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
