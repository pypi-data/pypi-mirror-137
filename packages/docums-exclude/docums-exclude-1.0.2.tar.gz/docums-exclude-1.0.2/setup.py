import os.path
import setuptools
from setuptools import setup

def read(name):
    mydir = os.path.abspath(os.path.dirname(__file__))
    return open(os.path.join(mydir, name)).read()


setuptools.setup(
    name='docums-exclude',
    version='1.0.2',
    packages=['docums_exclude'],
    url='https://github.com/khanhduy1407/docums-exclude',
    license='Apache',
    author='NKDuy',
    author_email='kn145660@gmail.com',
    description='A docums plugin that lets you exclude files or trees.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=['docums'],

    # The following rows are important to register your plugin.
    # The format is "(plugin name) = (plugin folder):(class name)"
    # Without them, docums will not be able to recognize it.
    entry_points={
        'docums.plugins': [
            'exclude = docums_exclude:Exclude',
        ]
    },
)
