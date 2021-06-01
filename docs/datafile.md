# datafile
Помогает работать с информацией без написания дополнительных функций</br>
Находится в `vkuserbot.utils`

## datafile
```
TOKEN=YOUR_TOKEN
```

## main.py
```python
from vkuserbot.user import User, Message
from vkuserbot.utils import get_datafile

datafile = get_datafile() #Возвращает словарь
bot = User(datafile["TOKEN"])

@bot.handle(text=["hello"])
async def sayhello(mes: Message):
    await mes.reply("Привет")

if __name__ == "__main__":
    bot.run()
```