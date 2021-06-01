import aiohttp


async def post(link: str, data: dict) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(link, data=data) as response:
            return await response.json(content_type=None)
