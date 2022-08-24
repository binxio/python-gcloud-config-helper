#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ "python-dateutil", "google-auth", "pytz" ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Mark van Holsteijn",
    author_email='markvanholsteijn@binx.io',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="obtain Google GCloud configuration credentials",
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='gcloud_config_helper',
    name='gcloud_config_helper',
    packages=find_packages(include=['gcloud_config_helper', 'gcloud_config_helper.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/binxio/python-gcloud-config-helper',
    version='0.3.1',
    zip_safe=False,
)
