import pecan
from pecan import rest
from pecan_swagger import decorators as swagger
import wsme
from wsme import types as wtypes
from wsmeext.pecan import wsexpose


class MessageModel(object):
    id = wtypes.StringType(min_length=1, max_length=255)
    message = wtypes.StringType(min_length=1, max_length=255)
    message_size = wtypes.IntegerType(minimum=1)
    message_from = wtypes.Enum(str, '1.OSOMATSU', '2.KARAMATSU',
                               '3.CHOROMATSU', '4.ICHIMATSU',
                               '5.JUSHIMATSU', '6.TODOMATSU')


class MessageCollection(object):
    messages = [MessageModel]

@swagger.path('wsmemessages', 'WsmeMessages', 'WsmeRoot')
class MessagesController(rest.RestController):

    _custom_actions = {
        'detail': ['GET'],
    }

    @wsexpose(MessageCollection)
    def get_all(self):
        return MessageCollection()

    @wsexpose(MessageModel, wtypes.text)
    def get_one(self, id):
        return MessageModel()

    @wsexpose(MessageModel, wtypes.text, status_code=201)
    def post(self, message):
        return MessageModel()

    @wsexpose(None, wtypes.text, status_code=204)
    def delete(self, id):
        pass

    @wsexpose(MessageModel, wtypes.text)
    def detail(self, id):
        return MessageModel()

@swagger.path('/', 'WsmeRoot')
class RootController(rest.RestController):
    pass
