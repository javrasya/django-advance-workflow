__author__ = 'ahmetdal'

from setuptools import setup

try:
    long_description = open('README.md').read()
except IOError:
    long_description = ''

setup(
    name='django-advance-workflow',
    version='1.0.0',
    description='Django complex workflow support.',
    author='Ahmet DAL',
    author_email='ceahmetdal@gmail.com',
    url='https://bitbucket.org/ahmetdal/django-advance-workflow',
    keywords=["django", "workflow"],
    install_requires=[
        "Django",
    ],
    packages=['daw','daw.models','daw.models.managers','daw.models.querysets','daw.service','daw.templatetags','daw.tests','daw.utils'],
    include_package_data=True,
    zip_safe=False,
    license='GPL',
    platforms=['any'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ]
)
