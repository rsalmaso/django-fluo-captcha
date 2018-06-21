#!/usr/bin/env python3

from setuptools import setup, find_packages
import io
import captcha


with io.open("README.md", "rt", encoding="utf-8") as fp:
    long_description = fp.read()


setup(
    packages=find_packages(),
    include_package_data=True,
    name="django-fluo-captcha",
    version=captcha.__version__,
    description="captha widget for django apps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=captcha.__author__,
    author_email=captcha.__email__,
    url="https://bitbucket.org/rsalmaso/django-fluo-captcha",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: JavaScript",
    ],
    install_requires=["django"],
    zip_safe=False,
)
