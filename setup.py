from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='domestic-violence-tracker',
    version='0.1.0',
    description='Attempted to standardized available FBI data on domesitc violence',
    long_description=readme,
    author='Luke Whyte',
    author_email='lwhyte@express-news.net',
    url='https://github.com/lukewhyte/domestic-violence-tracker',
    license=license,
    packages=find_packages(exclude=('tests'))
)