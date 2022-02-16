from setuptools import setup, find_packages
import codecs
import os

VERSION='0.0.01'
DESCRIPTION="Wki terminal!"
LONG_DESCRIPTION="# Who don't like terminal,\n now you can exploer wikipedia in terminal!"
setup(
    name="Terminal_wikipedia",
    version=VERSION,
    author='random guy from internet',
    author_email='j*****.*****@gmail.com',
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests','rich','bs4'],
    keywords=['python','tool','terminal app','wikipedia'],
    classifiers=[
        'Development :: mayby later (planning)',
        "Intended Audienc :: terminal lovers",
        'Programing Language :: python :: 3',
        "Operating System :: Microsoft :: Windows"

    ]

)
