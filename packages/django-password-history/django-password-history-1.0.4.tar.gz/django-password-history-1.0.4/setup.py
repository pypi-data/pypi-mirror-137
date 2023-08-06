#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(*file_paths):
    """Retrieves the version from django_password_history/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version("django_password_history", "__init__.py")


if sys.argv[-1] == 'publish':
    try:
        import wheel
        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on git:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.md').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')
requirements = open('requirements.txt').readlines()

setup(
    name='django-password-history',
    version=version,
    description="""Django module meant to allow django users to keep a history of their previously used passwords.""",
    long_description_content_type='text/markdown',
    long_description=readme + '\n\n' + history,
    author='Roderick Smith',
    author_email='smithroderick17@gmail.com',
    url='https://github.com/Lenders-Cooperative/django-password-history',
    download_url='https://github.com/Lenders-Cooperative/django-password-history/archive/refs/tags/vf.tar.gz',
    packages=[
        'django_password_history',
    ],
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='django-password-history',
    classifiers=[
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
