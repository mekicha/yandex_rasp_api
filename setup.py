import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="yandex.rasp",
    version="0.0.1",
    author="Emeka Icha",
    author_email="emeka.icha@gmail.com",
    description="A Python wrapper for Yandex.Schedules API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="yandex yandex.rasp rest",
    url="https://github.com/mekicha/yandex-rasp-api",
    packages=setuptools.find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)
