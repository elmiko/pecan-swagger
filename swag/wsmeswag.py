from wsme import types as wtypes
import inspect

_definitions = {}

_x = []

def getpaths(methods):
    paths = {path: {methodname: getmethodattr(methods[path][methodname])
                            for methodname in methods[path]}
                     for path in methods}
    return paths

def getmethodattr(method):
    _x.append(method)
    __comments__ = [s.strip() for s in str(method.__doc__).splitlines()]
    attr = {}
    attr['description'] = "".join(__comments__[1:])
    attr['produces'] = [method._pecan['content_type']]
    attr['summary'] = __comments__[0]
    attr['responses'] = getresponses(method)
    attr['parameters'] = getparameters(method)
    return attr

def getresponses(method):
    responses = {}
    wmethod = method._wsme_definition
    code = wmethod.status_code

    responses[code]={'description':'success',
                     'schema':getschema(wmethod.return_type)}
    return responses

def getschema(return_type):
    schema = {}
    if type(return_type) == type(wtypes.Base):
        name = "".join(e for e in str(return_type).split('.')[-1] if e.isalnum())
        schema['$ref'] = "#/definitions/" + name
        if not name in _definitions:
            _definitions[name] = {}
            _definitions[name]['type'] = 'object'
            _definitions[name]['xml'] = {"name":name}
            _definitions[name]['properties'] = {}
            for attr in dir(return_type):
                if isinstance(getattr(return_type, attr), wtypes.wsattr):
                    _definitions[name]['properties'][attr] = getschema(getattr(return_type, attr))
    elif isinstance(return_type, wtypes.wsattr):
        if (isinstance(return_type.datatype, wtypes.ArrayType)):
            schema['type'] = 'array'
            schema['items'] = getschema(return_type.datatype.item_type)
        elif type(return_type.datatype) == type(wtypes.Base):
            schema = getschema(return_type.datatype)
        else:
            schema = gettype(return_type.datatype)
    elif isinstance(return_type, wtypes.ArrayType):
        schema['type'] = 'array'
        schema['items'] = getschema(return_type.item_type)

    return_types = [attr for attr in dir(return_type)
                    if isinstance(getattr(return_type, attr), wtypes.wsattr)]
    return schema

def getparameters(method):
    """
    retrieves the parameters passed into a controller method
    :param method:
    :return: dictionary of controller parameters in swagger format
    """
    parameters = []
    for arg in method._wsme_definition.arguments:
        argspec = {}
        if type(arg.datatype) == type(wtypes.Base):
            argspec['name'] = "".join(e for e in str(arg.datatype).split('.')[-1] if e.isalnum())
            argspec['schema'] = getschema(arg.datatype)
            argspec['in'] = "body"
            argspec['description'] = inspect.getdoc(arg.datatype)
            argspec['required'] = True
        else:
            argspec['name'] = arg.name
            argspec['in'] = "path"
            description = [x for x in inspect.getdoc(method).split("\n")
                           if (x.split(" ")[0] == str("param: " + arg.name), None)]
            argspec['description'] = description[0]
            argspec['required'] = True
            argspec['type'] = "string"
        parameters.append(argspec)
    return parameters

def gettype(datatype):
    """
    given a datatype, return a dictionary with the swagger type and format the datatype belongs to
    :param datatype:
    :return: swagger type spec
    """
    schema = {}
    if datatype == wtypes.IntegerType or "Integer" in str(datatype):
        schema['type'] = 'integer'
        schema['format'] = str(datatype)
    else:
        schema['type'] = 'string'
        schema['format'] = str(datatype)
    return schema
