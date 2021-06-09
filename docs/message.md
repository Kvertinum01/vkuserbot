# Message
Класс, описывющий сообщение
## Функции класса
`answer` - написать сообщение в чат, из которого было получено сообщение <br/>
`reply` - ответить на сообщение, на которое отреагировал бот <br/>
`get_photo` - получть фотографию из сообщения, на которое отреагировл бот
## Пример использования
```python
from vkuserbot import User, Message

...

@bot.handle()
async def _(mes: Message):
    await mes.answer("Hello")

...

```
