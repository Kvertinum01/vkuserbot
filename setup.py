from setuptools import setup

name = "vkuserbot"
version = "0.0.4"

setup(
    name=name,
    version=version,
    packages=["vkuserbot"],
    install_requires=[
        "aiohttp",
        "aiosqlite",
        "aiofiles"
    ],
)
