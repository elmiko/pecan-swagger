import json
import restswag
import wsmeswag
import inspect

# import your projects root controller here:
# from ____ import ____ as RootController

_c = []

def collect_swagger(title, version):
    swagger = {}
    swagger['swagger'] = '2.0'
    swagger['info'] = {    'title': title,
                            "description": str(inspect.getcomments(RootController)),
                            'version': version,
                            "license": {
                                "name": "Apache 2.0",
                                "url": "http://www.apache.org/licenses/LICENSE-2.0.html"
                            }
    }
    swagger['host'] = "google.com"
    swagger['schemes'] = ['http']
    swagger['basePath'] = '/'
    swagger['produces'] = ['application/json']

    controllers = restswag.collect_controllers(RootController)
    _c.append(controllers)
    methods = restswag.collect_methods(controllers)

    paths = wsmeswag.getpaths(methods)
    swagger['paths'] = paths

    definitions = wsmeswag._definitions
    swagger['definitions'] = definitions

    print json.dumps(swagger, indent=2)

# run below method with name and version and scooop up swagger from terminal
# collect_swagger(project_name, project_version)

collect_swagger("My_project", "1.0.0")