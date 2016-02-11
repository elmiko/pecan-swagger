import setuptools

from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))
# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()


setuptools.setup(
    name='pecan-swagger',
    version='0.1.0',
    description='A project to produce swagger from pecan',
    long_description=long_description,
    url='https://github.com/elmiko/pecan-swagger',
    author='Michael McCune',
    author_email='msm@opbstudios.com',
    license='BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        ],
    keywords='pecan swagger development',
    packages=[
        'pecan_swagger',
    ],
)
