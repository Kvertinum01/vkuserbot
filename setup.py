from setuptools import setup

name = "vkuserbot"
version = "0.0.3"

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
