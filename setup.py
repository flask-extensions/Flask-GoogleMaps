# coding: utf8

from setuptools import setup, find_packages

setup(
    name='Flask-GoogleMaps',
    version='0.2.0',
    license='MIT',
    description='Small extension for Flask to make using Google Maps easy',
    long_description=open('README.md').read(),
    author='Bruno Rocha',
    author_email='rochacbruno@gmail.com',
    url='https://github.com/rochacbruno/Flask-GoogleMaps/',
    platforms='any',
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=['Flask'],
    packages=find_packages()
)
