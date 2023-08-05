import pathlib
import re
from setuptools import setup

HERE = pathlib.Path(__file__).parent
readme = (HERE / 'README.md').read_text()

packages = [
    'toontown',
    'toontown.models'
]


def requirements():
    with open('requirements.txt') as file:
        return file.read().splitlines()


def version():
    with open('toontown/__init__.py') as f:
        return re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)


setup(
    name='toontown.py',
    author='jaczerob',
    url='https://github.com/jaczerob/toontown.py',
    version=version(),
    packages=packages,
    license='MIT',
    description='A simple Python wrapper for the Toontown Rewritten API',
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=requirements(),
    python_requires='>=3.8.0',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
