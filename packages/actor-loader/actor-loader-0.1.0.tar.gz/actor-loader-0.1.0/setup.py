import setuptools
from setuptools import setup

with open("README.md", 'r') as readme:
    long_description = readme.read()

setup(
    name='actor-loader',
    version='0.1.0',
    authour='Arch Leaders',
    authour_email='archleadership28@gmail.com',
    description='Console application to load the required C-Actors into any mod.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ArchLeaders/ActorLoader',
    include_package_data=True,
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts':
            ['actor-loader = src.actor_loader:main']
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires=">=3.7",
    install_requires=['bcml>=3.0.0']
)