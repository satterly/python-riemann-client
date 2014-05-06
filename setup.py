#!/usr/bin/env python

import setuptools

setuptools.setup(
    name="python-riemann-client",
    version='1.0.0',
    description='Riemann client',
    url='https://github.com/satterly/python-riemann-client',
    license='Apache License 2.0',
    author='Nick Satterly',
    author_email='nick.satterly@gmail.com',
    packages=setuptools.find_packages(exclude=['bin', 'tests']),
    install_requires=[
        'bernhard'
    ],
    include_package_data=True,
    zip_safe=True,
    scripts=['bin/riemann-client'],
    keywords='riemann client',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Topic :: System :: Monitoring'
    ]
)
