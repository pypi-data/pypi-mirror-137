from setuptools import setup,find_packages


setup(
name='steam_jack',
version='0.0.5',
author='Bert Van Acker',
author_email='bva.bmkr@gmail.com',
packages= find_packages(),      # NEW: find_packaged() for discovering hierarchical package OLD:['steam_jack'],
url='https://github.com/BertVanAcker/steam-jack.git',
license='LICENSE.txt',
description='Steam-jack development interface',
scripts=['steam_jack/Communicator/Communicator.py','steam_jack/Communicator/Communicator_Constants.py','steam_jack/Logger/Logger.py','steam_jack/DeviceLibrary/Emlid_navio.py'],
long_description=open('README.md').read(),
install_requires=[
   "serial"
],
)
