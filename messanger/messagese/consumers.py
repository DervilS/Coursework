from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from messagese.views import add_message, get_user
import json
from asgiref.sync import sync_to_async, async_to_sync

#Класс обработки сообщений по протоколу Websocket
class Messageconsumer(WebsocketConsumer):
    #Функция приема подключения по websocket
    def connect(self):
        #Получаем номер подключившегося пользователя и друга с которым он ведет переписку
        self.user_id = int(self.scope['url_route']['kwargs']['user_id'])
        self.receiver = get_user(self.user_id)
        #Запоминаем имя соединения как имена пользователей разделенных дефисом
        self.group_name = '-'.join(map(str, sorted([self.user_id, self.scope['user'].id])))
        #Добавляем соединение в общий список и одобряем подключение
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.accept()

    #Функция обработки отключения пользователя
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)

    #Функция обработки получения нового сообщения
    def receive(self, text_data):
        #Получем текст сообщения и добавлем его в БД
        message_data = json.loads(text_data)
        message = add_message(message_data ['text'], self.scope['user'], self.receiver)
        #Отправляем полученное сообщение другим пользователям в соединении
        async_to_sync(self.channel_layer.group_send)(self.group_name, {'message': message.text, 'sender':self.scope['user'].username , 'type': 'send.message'})

    def send_message(self, event):
        #Отправка сообщения другим пользователям в соединении
        message = event['message']
        self.send(text_data=json.dumps({'message': message, 'sender': event['sender']}))