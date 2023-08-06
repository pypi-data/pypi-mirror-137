from setuptools import setup, find_packages

classifiers = [
    'Programming Language :: Python :: 3',
	'Development Status :: 2 - Pre-Alpha',
    'License :: OSI Approved :: MIT License',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
]

setup(
name = 'toritpreprocess',
version = '0.0.1',
description = 'Some functions i continuously use and change',
url = '',
author = 'Tor Inge Thorsen',
author_email = 'tor.i.thorsen@ntnu.no',
license = 'MIT',
long_description = open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
long_description_content_type = 'text/markdown',
packages = find_packages(),
classifiers = classifiers,
keywords='processing',
install_requires=['']
)