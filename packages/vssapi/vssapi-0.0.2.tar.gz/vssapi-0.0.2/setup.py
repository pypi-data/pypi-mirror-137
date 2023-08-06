from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

VERSION = '0.0.2' 
DESCRIPTION = 'VSS API package'

# Setting up
setup(
        name="vssapi", 
        version=VERSION,
        author="Jure Jancigaj",
        author_email="falcon2k16@gmail.com",
        description=DESCRIPTION,
        long_description=long_description,
        long_description_content_type ="text/markdown",
        package_dir={"": "src"},
        py_modules=["vss"],
        install_requires=['requests', 'requests-toolbelt', 'python-dotenv'],
        keywords=['vss'],
        classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',

        'Topic :: Software Development :: Libraries :: Python Modules',

        'License :: OSI Approved :: MIT License',

        'Operating System :: OS Independent',

        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        ],
    )
