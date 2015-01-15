# pecan-swagger
some helpers to create swagger output from a pecan app

## example usage

given a file name `myapp.py`

    import pecan
    from pecan_swagger import decorators as swagger


    @swagger.path('profile', 'Profile', 'Root')
    class ProfileController(object):

        @swagger.method('GET')
        @pecan.expose(generic=True, template='index.html')
        def index(self):
            return dict()

        @swagger.method('POST')
        @index.when(method='POST')
        def index_post(self, **kw):
            print(kw)
            pecan.redirect('/profile')


    @swagger.path('/', 'Root')
    class RootController(object):

        profile = ProfileController()

and another file named `myapp-doc.py`

    from pecan_swagger import utils
    import myapp

    print(utils.swagger_build('myapp', '1.0'))

the following will be produced when run

    $ python myapp-doc.py
    {
      "swagger": "2.0",
      "info": {
        "version": "1.0",
        "title": "myapp"
      },
      "paths": {
        "/profile": {
          "POST": {},
          "GET": {}
        },
        "/": {}
      }
    }
