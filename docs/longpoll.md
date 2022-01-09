# Longpoll
Расположение: `vkuserbot.longpoll` <br/>
На вход принимает 1 значение: <br/>
&nbsp; `bot` - класс `User` (vkuserbot.user) <br/>

## Пример использоания
```python
from vkuserbot import User, Longpoll

user = User("User token here")
longpoll = Longpoll(user) # ИЛИ user.longpoll

async def some_func():
    for message in longpoll.listener():
        print(message)

if __name__ == "__main__":
    user.loop.run_until_complete(some_func())
```