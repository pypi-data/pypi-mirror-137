from setuptools import setup

with open('readMe.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name                            = 'pyneospider',
    version                         = '0.0.1',
    description                     = 'python NeoSpider library',
    long_description                = long_description,
    long_description_content_type   = 'text/markdown',
    url                             = 'https://github.com/Neo3ds/pyneospider.git',
    author                          = 'TaeJuneJoung',
    author_email                    = 'jtj0525@gmail.com',
    install_requires                = ['pyserial'],
    license                         = 'MIT',
    packages                        = ['pyneospider'],
    zip_safe                        = False,
    classifiers                     = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires                 = '>=3.6',
)