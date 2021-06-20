from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = "0.2.0"

setup(
    name="vkuserbot",
    author="Kvertinum01",
    url="https://github.com/Kvertinum01/vkuserbot",
    description="Easy asynchronous VK API mini-framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=version,
    packages=["vkuserbot"],
    install_requires=[
        "aiohttp",
        "aiofiles"
    ],
    classifiers=[
		"Programming Language :: Python :: 3.8",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
    python_requires='>=3.7',
)
