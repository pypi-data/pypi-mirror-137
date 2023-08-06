from setuptools import setup

setup(
name='steam_jack',
version='0.0.3',
author='Bert Van Acker',
author_email='bva.bmkr@gmail.com',
packages=['steam_jack'],
url='https://github.com/BertVanAcker/steam-jack.git',
license='LICENSE.txt',
description='Steam-jack development interface',
scripts=['steam_jack/Communicator/Communicator.py','steam_jack/Communicator/Communicator_Constants.py','steam_jack/Logger/Logger.py'],
long_description=open('README.md').read(),
install_requires=[
   "serial"
],
)
