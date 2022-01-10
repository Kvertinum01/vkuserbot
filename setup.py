from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

__version__ = "1.1.1"
__author__ = "Kvertinum01"

setup(
    name="vkuserbot",
    author=__author__,
    url="https://github.com/Kvertinum01/vkuserbot",
    description="Easy asynchronous VK API mini-framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=__version__,
    packages=["vkuserbot"],
    install_requires=[
        "aiohttp",
        "aiofiles"
    ],
    classifiers=[
		"Programming Language :: Python :: 3.7",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
    python_requires='>=3.7',
)
