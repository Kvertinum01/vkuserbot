# Waiter
Класс, который позволяет получть ввод от пользователя
## Использование
`new` - декоратор, аргументом принимает айди waiter'a <br/>
`add` - добавляет пользователя в waiter, аргументами принимает peer_id и id waiter'а
`exit_waiter` - удаляет пользователя из waiter'а, на вход принимает только peer_id
## Пример использования
```python
from vkuserbot import User, Waiter

bot = User("User token here")
waiter = Waiter()

@waiter.new(1)
async def simple_waiter(mes):
    if mes.data["text"] == "exit":
        waiter.exit_waiter(mes.data["peer_id")
    else:
        await mes.answer(mes.data["text"])

@bot.handle(text=["waiter"])
async def add_to_waiter(mes):
    await mes.answer("Напишите любое сообщение или exit чтобы выйти")
    waiter.add(mes.data["from_id"], 1)

if __name__ == "__main__":
    bot.waiter = waiter
    bot.run()
```