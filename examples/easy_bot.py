from vkuserbot import User, Message, gen_token, get_datafile
import os

get_datafile(".env")

token = gen_token(
    os.getenv("LOGIN"),
    os.getenv("PASSWORD")
)
user = User(token)

@user.handle(cmd=["/eat"])
async def eat_something(mes: Message, cmd_args: list):
    item = cmd_args[0]
    await mes.reply("Вы съели {}".format(item))

if __name__ == "__main__":
    user.run()