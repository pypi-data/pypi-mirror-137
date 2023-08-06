from setuptools import setup, find_packages
classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name="scramblery",
    version="1.0.0",
    author="Enes Altun",
    author_email="enesaltun2@gmail.com",
    description="A simple tool to scramble your images or only faces from images or videos",
    license="MIT",
    package=find_packages(),
    python_requires=">=3.5"

    )