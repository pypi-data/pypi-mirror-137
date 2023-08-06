from setuptools import setup, find_packages

setup(
    name="dbabget",
    version="0.101",
    author="huzi",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "dbabget = dbabget.dbabget:main",
        ]
    },
    license="MIT",
    description="An awesome package that does something",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "beautifulsoup4 >= 4",
    ],
)
