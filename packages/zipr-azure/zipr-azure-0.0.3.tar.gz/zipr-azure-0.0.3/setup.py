from setuptools import setup, find_namespace_packages

setup(
    name='zipr-azure',
    version='0.0.3',
    author='Andrew Hoekstra',
    author_email='andrew@pointevector.com',
    url='https://github.com/Pointe-Vector/zipr',
    packages=find_namespace_packages(include=['zipr.*']),
    install_requires=[
        'zipr-core',
    ],
    entry_points={'zipr.plugins': 'Azure = zipr.azure'},
)
