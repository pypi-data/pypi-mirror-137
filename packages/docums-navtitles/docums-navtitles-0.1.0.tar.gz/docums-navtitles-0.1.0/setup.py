
from distutils.core import setup

setup(
    name='docums-navtitles',
    version='0.1.0',
    author='NKDuy',
    author_email='kn145660@gmail.com',
    packages=['docums_navtitles'],
    license='LICENSE.txt',
    description='Docums plugin that loads all page titles from source.',
    install_requires=[
    ],

    entry_points={
        'docums.plugins': [
            'navtitles = docums_navtitles:NavTitleLoader',
        ]
    }
)

