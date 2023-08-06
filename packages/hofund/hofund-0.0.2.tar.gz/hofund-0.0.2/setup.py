from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name = 'hofund',
    version = '0.0.2',
    author = 'Ramey Girdhar',
    author_email = 'ramey.girdhar@gojek.com',
    license = 'UNLICENSED',
    description = 'allows user to search protos using stencil',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://source.golabs.io/asgard/spikes/prototypes/hofund',
    py_modules = ['hofund'],
    packages = find_packages(),
    install_requires = [
        'aiohttp',
        'aiodns',
        'cchardet',
        'pandas'
    ],
    python_requires='>=3.10',
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    entry_points = '''
        [console_scripts]
        hofund=hofund:main
    '''
)