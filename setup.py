import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-easy-api',
    version='0.3.0',
    packages=['easy_api'],
    install_requires=[''],
    include_package_data=True,
    license='MIT License',
    description='Create an API for you Django project with only a single line of code!',
    long_description=README,
    url='https://github.com/Miserlou/django-easy-api',
    author='Rich Jones',
    author_email='rich@openwatch.net',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
