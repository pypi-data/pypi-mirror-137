from setuptools import setup, find_namespace_packages

setup(
    name='zipr-http',
    version='0.0.1',
    packages=find_namespace_packages(include=['zipr.*']),
    # install_requires=[
    #     'zipr-core',
    # ],
    entry_points={'zipr.plugins': 'Http = zipr.http'},
)
