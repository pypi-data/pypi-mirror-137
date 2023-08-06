# -*- coding: utf-8 -*-
from setuptools import setup

with open("README.md") as f:
    readme = f.read()

setup(
    name="DocumsAwesomeListPlugin",
    version="0.1.0",
    description="Docums Plugin to inject social media cards for each entry in an awesome-list.",
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords=["docums", "plugin", "awesome", "list"],
    author="NKDuy",
    author_email="kn145660@gmail.com",
    url="https://github.com/khanhduy1407/docums-awesome-list-plugin",
    license="MIT license",
    packages=["docums_awesome_list_plugin"],
    install_requires=["docums", "webpreview>=1.6.0"],
    python_requires=">=3.4, <4",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    # This entry point is necessary for Docums to be able to use the plugin
    entry_points={
        'docums.plugins': [
            'awesome-list = docums_awesome_list_plugin.awesomelist:AwesomeList',
        ]
    },
)
