from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="valid_typing",
    version="0.2.3",
    description="A simple typing validator",
    long_description=long_description,
    url="https://gitlab.com/WilliamWCYoung/valid-typing",
    author="William Young",
    author_email="william.w.c.young@hotmail.com",
    license="MIT",
    packages=["valid_typing"],
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=[],
    python_requires=">=3.9",
    download_url="https://gitlab.com/WilliamWCYoung/valid-typing/-/archive/0.1.0/valid-typing-0.1.0.tar.gz",
)
