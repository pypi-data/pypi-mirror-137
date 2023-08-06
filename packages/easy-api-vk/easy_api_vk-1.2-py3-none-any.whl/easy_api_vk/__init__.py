import os

try:
    import vk_api as vk
    import colorama
    from colorama import Fore
    colorama.init()
except Exception as e:
    print(e)
    result = 0
    if str(e) ==  "No module named 'vk_api'":
        result = 1
    elif str(e) == "No module named 'colorama'":
        result = 2
    else:
        pass
    
    if result == 1:
        os.system("pip install vk_api")
    if result == 2:
        os.system("pip install colorama")


class helper:
    def clear(why = None):
        if why == None:
            why = input("Y/n \n")
        if why.lower() == "y":
            os.system('cls')
        else:
            print("Отказ")
  
    
    def err(text):
        print("Вы не указали{} {}{}". format(Fore.BLUE, text, Fore.RESET))


class connect:
    def __init__(self, token):
        global vk_api
        vk_api = vk.VkApi(token = token)


class status:
    def get(id: int = None):
        if id == None:
            helper.err("id status.get")
        else:
            return vk_api.method("status.get", {
                "user_id": id
            })["text"]


    def set(text: str = None):
        if text == None:
            helper.err("text status.set")
        else:
            vk_api.method("status.set", {
                "text": text
            })


class account:
    def ban(id:int = None):
        if id == None:
            helper.err("id account.ban")
        else:
            try:
                result = vk_api.method("account.ban", {
                    "owner_id": id
                })
            except Exception as e:
                if str(e) == "[15] Access denied: user already blacklisted":
                    result = 2
                elif str(e) == "Captcha needed":
                    result = 3
                else:
                    pass
                

            if result == 1:
                print(Fore.GREEN + "Успешно" + Fore.RESET)
            elif result == 2:
                print(Fore.GREEN + "Пользователь уже внесен в черный список" + Fore.RESET)
            elif result == 3:
                print(Fore.RED + "Капча" + Fore.RESET)

        return result
                

    def unban(id:int = None):
        if id == None:
            helper.err("id account.unban")
        else:
            try:
                result = vk_api.method("account.unban", {
                    "owner_id": id
                })
            except Exception as e:
                print(e)
                if str(e) == "[15] Access denied: user not blacklisted":
                    result = 2
                elif str(e) == "Captcha needed":
                    result = 3
                else:
                    pass
            

            if result == 1:
                print(Fore.GREEN + "Успешно" + Fore.RESET)
            elif result == 2:
                print(Fore.GREEN + "Пользователь уже вынесен из черного списка" + Fore.RESET)
            elif result == 3:
                print(Fore.RED + "Капча" + Fore.RESET)
                
        return result


class friends:
    def add(id:int = None):
        if id == None:
            helper.err("id friends.add")
        else:
            try:
                result = vk_api.method("friends.add", {
                    "user_id": id
                })
            except Exception as e:
                print(e)
                if str(e) == "[174] Cannot add user himself as friend":
                    result = 174
                elif str(e) == "[175] Cannot add this user to friends as they have put you on their blacklist":
                    result = 175
                elif str(e) == "[176] Cannot add this user to friends as you put him on blacklist":
                    result = 176
                elif str(e) == "[177] Cannot add this user to friends as user not found":
                    result = 177
                elif str(e) == "Captcha needed":
                    result = 178
                else:
                    pass

            if result == 1:
                print(Fore.GREEN + "Успешно" + Fore.RESET)
            elif result == 2:
                print(Fore.GREEN + "Заявка принята" + Fore.RESET)
            elif result == 4:
                print(Fore.GREEN + "Повторите попытку" + Fore.RESET)
            elif result == 174:
                print(Fore.YELLOW + "Не удалось добавить в друзья" + Fore.RESET)
            elif result == 175:
                print(Fore.YELLOW + "Вы в черном списке пользователя" + Fore.RESET)
            elif result == 176:
                print(Fore.YELLOW + "Не удается добавить этого пользователя в друзья, так как вы занесли его в черный список" + Fore.RESET)
            elif result == 177:
                print(Fore.YELLOW + "Не удается найти пользователя, проверьте id" + Fore.RESET)
            if result == 178:
                print(Fore.RED + "Капча" + Fore.RESET)
        return result


    def delete(id:int = None):
        if id == None:
            helper.err("id friends.delete")
        else:
            try:
                result = vk_api.method("friends.delete", {
                    "user_id": id
                })
            except Exception as e:
                print(e)
                if str(e) == "Captcha needed":
                    result = 4
                else:
                    pass
            
            if result == "success":
                print(Fore.GREEN + "Друг успешно удален" + Fore.RESET)
            elif result == "friend_deleted":
                print(Fore.GREEN + "Друг был удален" + Fore.RESET)
            elif result == "out_request_deleted":
                print(Fore.GREEN + "Отменена исходящая заявка" + Fore.RESET)
            elif result == "in_request_deleted":
                print(Fore.GREEN + "Отклонена входящая заявка" + Fore.RESET)
            elif result == "in_request_deleted":
                print(Fore.GREEN + "Отклонена рекомендация друга" + Fore.RESET)
            elif result == 1:
                print(Fore.GREEN + "Пользователь удален из списка друзей" + Fore.RESET)
            elif result == 2:
                print(Fore.GREEN + "Заявка на добавление в друзья данного пользователя отклонена (входящая или исходящая)" + Fore.RESET)
            elif result == 3:
                print(Fore.GREEN + "Рекомендация добавить в друзья данного пользователя отклонена" + Fore.RESET)
            elif result == 4:
                print(Fore.RED + "Капча" + Fore.RESET)
        return result


    def get(id:int = None, order: str = None, count: int = None, offset: int = None, fields: str = None, name_case: str = None):
        if id == None:
            helper.err("id friends.get")
        else:
            try:
                result = vk_api.method("friends.get", {
                    "user_id": id, 
                    "order": order,
                    "count": count,
                    "offset": offset,
                    "fields": fields,
                    "name_case": name_case
                })
            except Exception as e:
                print(e)
                if str(e) == "[30] This profile is private":
                    result = 30
                elif str(e) == "[18] User was deleted or banned":
                    result = 18
                else:
                    pass

            if result == 30:
                print(Fore.YELLOW + "Профиль закрыт" + Fore.RESET)
            if result == 18:
                print(Fore.YELLOW + "Страница пользователя заблокирована или удалена" + Fore.RESET)

        return result


class gifts:
    def get(id:int = None):
        if id == None:
            helper.err("id gifts.get")
        else:
            try:
                result = vk_api.method("gifts.get", {
                    "user_id": id
                })
            except Exception as e:
                print(e)
                if str(e) == "[15] Access denied":
                    result = 15
                else:
                    pass

                if result == 15:
                    print(Fore.YELLOW + "Нет доступа" + Fore.RESET)
        return result
                

            
