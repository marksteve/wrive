from setuptools import setup


setup(
    name='wrive',
    version='0.0.1',
    packages=['wrive'],
    author="Mark Steve Samson",
    author_email='marksteve@insynchq.com',
    description="Simple Google Drive docs publishing",
    long_description=open('README.md').read(),
    install_requires=open('requirements.txt').read().split('\n'),
    include_package_data=True,
    zip_safe=False,
)
