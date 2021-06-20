# EmptyMiddleware
Класс для обработки данных
## Использование
Данный класс должен наследоваться другой класс <br>
Дочерний класс может иметь 2 метода: <br>
`before` - функция будет вызвана при событии сообщения от longpoll (async)<br>
`after` - функция будет вызвана при создании класса Message (sync)
## Пример
```python

from vkuserbot import ..., EmptyMiddleware

class MyMiddleware(EmptyMiddleware):
    async def begin(message: dict):
        message["text"] = message["text"].lower()
        return message

...

#bot: User
bot.middleware = MyMiddleware

#Теперь при получении любого сообщения к тексту всегда будет применяться .lower()

```