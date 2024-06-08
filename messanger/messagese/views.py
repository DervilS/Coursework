from django.shortcuts import render, redirect
from messagese.models import Message, Profile, FriendsList
from django.contrib.auth import login
from django.db.models import Q

#Функция conversation демонстрирует страницу мессенджера
def conversation(request, friend_id=None):
    #Если пользователь не залогинен отправляем его на страницу авторизации
    if not request.user.is_authenticated:
        return redirect("/login/")
    #Если id друга передан(не none), тогда получаем информацию у друге из БД
    try:
        friend=Profile.objects.get(id=friend_id)
    #Иначе пользователь впервые зашел на страницу и мы выбираем первого попавшегося друга из БД
    except Profile.DoesNotExist:
        friend=request.user.responsers.filter(is_accepted = True).first().user2
    #Если Пользователь отправил новое сообщение, вызываем функцию add message
    if request.method == "POST":
        text = request.POST["message"]
        add_message(text, request.user, friend)
    #Получаем список сообщений, где текущий пользователь является либо отправителем либо получателем, а его собеседником является выбранный друг
    message_list=Message.objects.filter(Q(sender=request.user) & Q(receiver=friend) | Q(receiver=request.user) & Q(sender=friend)).order_by("created_at")
    #Если возникла ошибка добавления пользователя в друзья(написано имя пользователя, которого нет в БД), тогда демонстрируем ошибку на странице
    error = None
    if "error" in request.GET:
        error = request.GET["error"]
    #Список друзей пользователя
    friends_list = FriendsList.objects.filter(Q(user1 = request.user) | Q(user2 = request.user), is_accepted = True)
    #Список запросов к пользователю на добавление в друзья
    new_friends_list = request.user.requesters.filter(is_accepted__isnull = True)
    #Список запросов от пользователя ожидающих подтверждение
    responsers_list = request.user.responsers.filter(is_accepted__isnull = True)
    #Формируем страницу с полученными данными
    return render(request, "conversation.html", {"message_list": message_list, "receiver":friend, "error":error, 'friends_list':friends_list, 'new_friends_list':new_friends_list, 'responsers_list':responsers_list})

#Функция добавления нового сообщения в базу
def add_message(text, sender, receiver):
    return Message.objects.create(text=text, sender=sender, receiver=receiver)

#Функция получения пользователя из базы по его номеру
def get_user(user_id):
    return Profile.objects.get(id=user_id)

#Функция регистрации нового пользователя
def register(request):
    #Если пользователь прислал данные о регистрации
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirm = request.POST["confirm"]
        #Проверка пароля и подтверждения
        if password != confirm:
            return render(request, "registration/register.html", {"error":"Пароль и подтверждение не совпадают"})
        #Добавление пользователя в БД
        user = Profile.objects.create_user(username=username, password=password)
        #Авторизуем пользователя и отправляем на главную страницу
        login(request, user)
        return redirect("/")
    #Если пользователь впервые на странице перенаправляем на стр регистрации
    return render(request, "registration/register.html")

#Функция добавления друга
def add_friend(request):
    #Если пользователь прислал данные для добавления другого пользователя в друзья
    if request.method == "POST":
        username = request.POST["name"]
        try:
            #Ищем выбранного пользователя в БД и добавляем связь между ними в таблицу друзей
            user = Profile.objects.get(username=username)
            request.user.friends.add(user)
        #Если пользователь не найден перенаправляем на страницу переписки с показанной ошибкой добавления
        except Profile.DoesNotExist:
            return redirect("/?error=пользователя с таким именем не существует")
        #Отправляем пользователя на страницу переписки
        return redirect(f"/{user.id}/")

#Функция изменения статуса запроса на дружбу
def change_friendship(user, friend_id, is_friend):
    #Получаем запросы из БД
    friendship_list = FriendsList.objects.filter(Q(user1 = user, user2_id = friend_id)|Q(user1_id = friend_id, user2 = user))
    #Проходим по всем запросам устанавливаем им статус и сохраняем в БД
    for friendship in friendship_list:
        friendship.is_accepted = is_friend
        friendship.save()

#Подтверждения запроса на дружбу
def accept_friend(request, friend_id):
    change_friendship(request.user, friend_id, is_friend = True)
    return redirect(f'/{friend_id}/')

#Отклонение запроса на дружбу
def reject_friend(request, friend_id):
    change_friendship(request.user, friend_id, is_friend = False)
    return redirect(f'/{friend_id}/')