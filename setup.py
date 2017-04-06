import os

from setuptools import setup, find_packages

setup(
    name='django-freeradio',
    version='0.0.0',
    description='Free radio for Django',
    author='Mark Steadman',
    author_email='mark@steadman.io',
    url='https://github.com/iamsteadman/django-freeradio',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    license='MIT',
    keywords='django radio',
    entry_points={
        'console_scripts': [
            'freeradio = freeradio.manage:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
