from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='docums-select-files',
    version='0.3.6',
    packages=['selectfiles'],
    license='Apache-2.0',
    author='NKDuy',
    author_email='kn145660@gmail.com',
    description='Filter pages for assignments',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/khanhduy1407/docums-select-files',
    install_requires=['docums'],

    entry_points={
        'docums.plugins': [
            'select-files = selectfiles.plugin:SelectFiles',
        ]
    },
)
