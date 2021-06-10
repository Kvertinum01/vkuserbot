import os
import asyncio
import aiohttp


def get_datafile(file_name: str = "datafile") -> None:
    with open(file_name, "r", encoding="utf-8") as file:
        info = file.read()
    for line in info.split("\n"):
        if "=" not in line or line[0] == "#":
            continue
        line_info = line.split("=")
        name, value = line_info[0], "=".join(line_info[1:])
        os.environ[name] = value


async def _post(link: str, data: dict) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(link, data=data) as response:
            return await response.json(content_type=None)


async def async_gen_token(login: str, password: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.post("https://oauth.vk.com/token", data={
            "grant_type": "password",
            "client_id": "2274003",
            "client_secret": "hHbZxrka2uZ6jB1inYsH",
            "username": login,
            "password": password
        }) as response:
            token_data = await response.json()
    assert "access_token" in token_data, token_data["error_description"]
    return token_data["access_token"]


def gen_token(login: str, password: str) -> str:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(
        async_gen_token(login, password)
    )
