import pecan
from pecan import rest
from pecan_swagger import decorators as swagger


@swagger.path('api', 'API', 'Root')
class APIController(rest.RestController):

   @pecan.expose()
   def get(self):
       pass


@swagger.path('messages', 'Messages', 'Root')
class MessagesController(object):

    @pecan.expose(generic=True, template='messages.html')
    def index(self):
        return list()

    @index.when(method='POST')
    def index_post(self, **kw):
        print(kw)
        pecan.redirect('/messages')


@swagger.path('profile', 'Profile', 'Root')
class ProfileController(object):

    @pecan.expose(generic=True, template='profile.html')
    def index(self):
        return dict()

    @index.when(method='POST')
    def index_post(self, **kw):
        print(kw)
        pecan.redirect('/profile')

    @pecan.expose(generic=True)
    def image(self):
        print('no image uploaded')

    @image.when(method='POST')
    def image_post(self):
        print('not supported')

    @pecan.expose()
    def stats(self):
        return dict()


@swagger.path('/', 'Root')
class RootController(object):

    profile = ProfileController()
    messages = MessagesController()
    api = APIController()
