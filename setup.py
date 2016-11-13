import os
from setuptools import setup
from normalized import VERSION

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setup(
    name='drf-normalized-serializer',
    version='.'.join(str(x) for x in VERSION),
    packages=['nomalized'],
    description='DRF normalized serializers',
    long_description=README,
    author='kimjeongin',
    author_email='kimjeongin92@gmail.com',
    url='https://bitbucket.org/mathpresso/normalized/',
    license='MIT',
    install_requires=[
        'Django>=1.8',
        'djangorestframework>=3.2',
    ],
    classifiers=[
        'Framework :: Django',
    ],
)
