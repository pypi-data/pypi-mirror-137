from setuptools import setup, find_packages

setup(
    name='PyRPoint',
    version='0.2',
    license='MIT',
    author="Anthony Kenny",
    author_email='anthonyjwkenny@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/AnthonyKenny98/example-publish-pypi',
    keywords='thinkcell powerpoint',
    install_requires=[],
)