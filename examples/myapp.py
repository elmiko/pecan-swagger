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
