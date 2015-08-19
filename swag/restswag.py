from pecan import rest
import inspect

def decorated_controllers():
    return []

def collect_controllers(RootController):
    """
    Traverses project starting with RootController
    and collects all RestControllers returning a tuple with their respective paths.
    Concatenates decorated controllers and their paths to the list.
    :return [(controllers, path),...]
    """
    stack = [(RootController, "/")]
    queue = []
    while stack:
        restcontroller = stack.pop()
        controllers = []
        for ctrl in dir(restcontroller[0]):
            if issubclass(type(getattr(restcontroller[0], ctrl)), rest.RestController):
                controllers.append((getattr(restcontroller[0], ctrl), ctrl))
        for controller in controllers:
            sep = '/'
            if restcontroller[1][-1] == sep: sep = ''
            stack.append((controller[0], restcontroller[1] + sep + controller[1]))
        queue.append(restcontroller)

    queue + decorated_controllers()
    return queue

def collect_methods(controllers):
    """
    collects all restful method paths from all restcontrollers in controllers
    and returns a dictionary with their method-names and methods.
    :return: {path: method-name: method}
    """
    methods = {}
    for controller in controllers:

        # going through standard pecan methods
        if getattr(controller[0], 'get_one', None):
            methodtuple = (controller[1] + "/{" +
                               getattr(controller[0], 'get_one')._pecan['argspec'][0][1] + "}",
                           ('get', getattr(controller[0], 'get_one')))
            methods = add_method(methods, methodtuple)
        if getattr(controller[0], 'get_all', None):
            methodtuple = (controller[1], ('get', getattr(controller[0], 'get_all')))
            methods = add_method(methods, methodtuple)
        if getattr(controller[0], 'get', None):
            methodtuple = (controller[1], ('get', getattr(controller[0], 'get')))
            methods = add_method(methods, methodtuple)
        if getattr(controller[0], 'new', None):
            pass
            methods = add_method(methods, methodtuple)
        if getattr(controller[0], 'edit', None):
            pass
            methods = add_method(methods, methodtuple)
        if getattr(controller[0], 'post', None):
            methodtuple = (controller[1], ('post', getattr(controller[0], 'post')))
            methods = add_method(methods, methodtuple)
        if getattr(controller[0], 'put', None):
            methodtuple = (controller[1], ('put', getattr(controller[0], 'put')))
            methods = add_method(methods, methodtuple)
        if getattr(controller[0], 'get_delete', None):
            methodtuple = (controller[1] +  "/{" +
                               getattr(controller[0], 'get_delete')._pecan['argspec'][0][1] + "}",
                           ('delete', getattr(controller[0], 'get_delete')))
            methods = add_method(methods, methodtuple)
        if getattr(controller[0], 'delete', None):
            methodtuple = (controller[1] +  "/{" +
                               getattr(controller[0], 'delete')._pecan['argspec'][0][1] + "}",
                           ('delete', getattr(controller[0], 'delete')))
            methods = add_method(methods, methodtuple)
        if getattr(controller[0], 'index', None):
            pass
        if getattr(controller[0], '_default', None):
            pass
        # pecan's _lookup function
        if getattr(controller[0], '_lookup', None):
            pass

        # if controller uses custom routing
        if getattr(controller[0], '_custom_actions', None):
            for k in controller[0]._custom_actions:
                m = getattr(controller[0], k, None)
                if m:
                    ml = [method in m]
                    for method in ml:
                        if method == 'get_one':
                            methodtuple = (controller[1] + "/{" +
                                           getattr(controller[0], 'get_one')._pecan['argspec'][0][1] + "}",
                           ('get', getattr(controller[0], 'get_one')))
                            methods = add_method(methods, methodtuple)
                            pass
                        elif method == 'get_delete':
                            methodtuple = (controller[1] + "/{" +
                                           getattr(controller[0], 'get_delete')._pecan['argspec'][0][1] + "}",
                           ('delete', getattr(controller[0], 'get_delete')))
                            methods = add_method(methods, methodtuple)
                            pass
                        elif method == 'delete':
                            methodtuple = (controller[1] + "/{" +
                                           getattr(controller[0], 'get_delete')._pecan['argspec'][0][1] + "}",
                           ('delete', getattr(controller[0], 'delete')))
                            methods = add_method(methods, methodtuple)
                        else:
                            methodtuple = (controller[1], (str(method).lower(), getattr(controller[0], k)))
                            methods = add_method(methods, methodtuple)

    return methods

def add_method(methods, methodtuple):
    path = methodtuple[0]
    methodname = methodtuple[1][0]
    methodfunction = methodtuple[1][1]
    if path not in methods:
        methods[path] = {}
    methods[path][methodname] = methodfunction
    return methods



import ast


def extract_return(file, fname):
    """
    tryna extract return type
    :param file:
    :param fname:
    :return:
    """
    for x in ast.walk(ast.parse(open(file).read())):
        if not(isinstance(x, ast.FunctionDef)):
            continue
        if not(x.name == fname):
            continue
        for b in x.body:
            if isinstance(b, ast.Return):
                if isinstance(b.value, ast.Name):
                    yield b.value.id