import threading
import json
from redis.exceptions import ConnectionError
from channels.generic.websocket import JsonWebsocketConsumer

from common.db.utils import close_old_connections
from common.utils import get_logger
from .site_msg import SiteMessageUtil
from .signals_handler import new_site_msg_chan

logger = get_logger(__name__)


class SiteMsgWebsocket(JsonWebsocketConsumer):
    refresh_every_seconds = 10
    chan = None

    def connect(self):
        user = self.scope["user"]
        if user.is_authenticated:
            self.accept()
            self.chan = new_site_msg_chan.subscribe()

            thread = threading.Thread(target=self.unread_site_msg_count)
            thread.start()
        else:
            self.close()

    def receive(self, text_data=None, bytes_data=None, **kwargs):
        data = json.loads(text_data)
        refresh_every_seconds = data.get('refresh_every_seconds')

        try:
            refresh_every_seconds = int(refresh_every_seconds)
        except Exception as e:
            logger.error(e)
            return

        if refresh_every_seconds > 0:
            self.refresh_every_seconds = refresh_every_seconds

    def send_unread_msg_count(self):
        user_id = self.scope["user"].id
        unread_count = SiteMessageUtil.get_user_unread_msgs_count(user_id)
        logger.debug('Send unread count to user: {} {}'.format(user_id, unread_count))
        self.send_json({'type': 'unread_count', 'unread_count': unread_count})

    def unread_site_msg_count(self):
        user_id = str(self.scope["user"].id)
        self.send_unread_msg_count()

        try:
            msgs = self.chan.listen()
            # 开始之前关闭连接，因为server端可能关闭了连接，而 client 还在 CONN_MAX_AGE 中
            close_old_connections()
            for message in msgs:
                if message['type'] != 'message':
                    continue

                try:
                    msg = json.loads(message['data'].decode())
                except json.JSONDecoder as e:
                    logger.debug('Decode json error: ', e)
                    continue
                if not msg:
                    continue

                logger.debug('New site msg recv, may be mine: {}'.format(msg))
                users = msg.get('users', [])
                logger.debug('Message users: {}'.format(users))
                if user_id in users:
                    self.send_unread_msg_count()
        except ConnectionError:
            logger.error('Redis chan closed')
        finally:
            logger.info('Notification ws thread end')
            close_old_connections()

    def disconnect(self, close_code):
        try:
            if self.chan is not None:
                self.chan.close()
            self.close()
        finally:
            close_old_connections()
            logger.info('Notification websocket disconnect')



