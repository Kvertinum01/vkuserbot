# datafile
Помогает работать с информацией без написания дополнительных функций</br>
Находится в `vkuserbot.utils`

## datafile
```
TOKEN=YOUR_TOKEN
```

## main.py
```python
from vkuserbot import User, Message, get_datafile
import os

get_datafile()
bot = User(os.environ["TOKEN"])

@bot.handle(text=["hello"])
async def sayhello(mes: Message):
    await mes.reply("Привет")

if __name__ == "__main__":
    bot.run()
```