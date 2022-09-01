import asyncio
import concurrent.futures

from pyfcm import FCMNotification

from app.config.consts import FCM_API_KEY

push_service = FCMNotification(api_key=FCM_API_KEY)


class PushMessageDto:
    def __init__(self, title, body):
        self.title = title
        self.body = body


def send_notification(registration_ids, message_title, message_body):
    return push_service.notify_multiple_devices(registration_ids=registration_ids,
                                                message_title=message_title,
                                                message_body=message_body)


async def send_push_alarm(user_tokens, message: PushMessageDto):
    loop = asyncio.get_event_loop()
    with concurrent.futures.ProcessPoolExecutor() as pool:
        await loop.run_in_executor(pool, send_notification, user_tokens, message.title, message.body)
