<h1 align="center">
  vkuserbot (1.x)
</h1>
<p align="center">
  <img src="https://img.shields.io/badge/made%20by-Kvertinum01-green">
  <img src="https://img.shields.io/badge/python-<3.7-orange">
  <img src="https://img.shields.io/badge/PyPI-v3.0-blue">
</p>

> Асинхронный мини-фреймворк для создания юзерботов VK

## Простой бот

```python
from vkuserbot import User, Message

user = User("User Token here")

@user.handle(text=["hello"])
async def say_hello(mes: Message):
    await mes.answer("Hello, world!")

if __name__ == "__main__":
    user.run()
```

 #### Больше примеров [здесь](https://github.com/Kvertinum01/vkuserbot/tree/master/exmaples)

## Установка
### Новейшая версия
```shell
pip install -U "git+https://github.com/Kvertinum01/vkuserbot#egg=vkuserbot"
```