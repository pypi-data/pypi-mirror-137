#!/usr/bin/env python3

"Create the package"

from setuptools import setup

setup(
    name='netdescribe',
    version='0.2.8',
    packages=['netdescribe',
              'netdescribe.snmp'],
    description='Library of functions for performing discovery on network devices.',
    long_description='Library of functions for performing discovery on network devices.',
    author='James Fleming',
    url='https://github.com/equill/netdescribe',
    author_email='james@electronic-quill.net',
    keywords=['network', 'discovery', 'snmp'],
    install_requires=['pysnmp==4.4.12'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking :: Monitoring',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9'],
    license='Apachev2'
)
