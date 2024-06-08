from django.urls import path, re_path
from messagese import consumers

#Адреса обработки запросов по протоколу websocket
websocket_urlpatterns=[re_path(r'^ws/messanger/(?P<user_id>\d+)/$', consumers.Messageconsumer.as_asgi())]