from setuptools import setup
from setuptools import find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='prnt',
    version='1.0.0',
    author='Keksiuwu',
    author_email='contact@keksi.me',
    license='MIT',
    description='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Keksiuwu/prnt',
    py_modules=['kawaiiapi'],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
