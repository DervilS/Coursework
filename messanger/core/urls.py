from django.contrib import admin
from django.urls import path, include
from messagese.views import conversation, register, add_friend, accept_friend, reject_friend
#Список адресов доступных на сайте, кажая запись в списке это url адрес и соответствующая ему функция обработчик из модуля views.py
#По этим адресам обрабатываются запросы по протоколу http

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("django.contrib.auth.urls")), 
    path("register/", register),
    path("<int:friend_id>/", conversation),
    path("", conversation),
    path("add_friend/", add_friend),
    path('accept/<int:friend_id>/', accept_friend),
    path('reject/<int:friend_id>/', reject_friend)
]