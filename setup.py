from setuptools import setup

name = "vkuserbot"
version = "0.0.4"

setup(
    author="Kvertinum01",
    url="https://github.com/Kvertinum01/vkuserbot",
    name=name,
    version=version,
    packages=["vkuserbot"],
    install_requires=[
        "aiohttp",
        "aiosqlite",
        "aiofiles"
    ],
)
