# handle_errors
<p>
  handle_errors - это словарь, в который первым аргументом принимает ошибку в формате строки,<br/>
  а вторым аргументом асинхронную функцию, которая будет вызываться при ошибке, которая была указна<br/>
  первым аргументом
</p>

## Пример использования
```python
from vkuserbot.user import User

bot = User("Your token here")

@bot.handle()
async def some_func(_):
    await bot.send(user_id=0) #Намеренно вызываем ошибку 100

async def handle_100(error):
    print("Произошла ошибка", error)

if __name__ == "__main__":
    bot.handle_errors = {
        "100": handle_100
    }
    bot.run()
```

Так же ошибки можно обрабатывать с помощью try-except
## Например
```python
from vkuserbot.user import User, VkApiError
bot = User("Your token here")
try:
    bot.send(user_id=0)
except VkApiError as e:
    print(e.code)
```