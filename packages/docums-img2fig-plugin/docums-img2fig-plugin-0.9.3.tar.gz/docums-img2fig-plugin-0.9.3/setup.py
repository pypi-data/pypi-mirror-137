# setup.py

import os
from setuptools import setup, find_packages

def read_file(fname):
    "Read a local file"
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='docums-img2fig-plugin',
    version='0.9.3',
    description='A Docums plugin that converts markdown encoded images into <figure> elements.',
	long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    keywords='docums python markdown',
    url='https://github.com/khanhduy1407/docums-img2fig-plugin',
    author='NKDuy',
    author_email='kn145660@gmail.com',
	license='MIT',
	python_requires='>=3.5',
    install_requires=[
		'docums'
	],
    packages=find_packages(),
    entry_points={
        'docums.plugins': [
            'img2fig = src:Image2FigurePlugin',
        ]
    }
)