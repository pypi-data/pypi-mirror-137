from setuptools import setup

setup(
    name='github-wiki-autosidebar',
    version='1.0.1',
    author='benrutter',
    description='Simple utility to generate a sidebar for github wikis',
    url='https://github.com/benrutter/github-wiki-autosidbar',
    packages=['autosidebar'],
    entry_points={
        'console_scripts': [
            'github-wiki-autosidebar = autosidebar.autosidebar:main',
        ],
    },
)

