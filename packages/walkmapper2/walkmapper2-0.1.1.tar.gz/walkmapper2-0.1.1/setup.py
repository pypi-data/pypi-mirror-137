from setuptools import setup, find_packages

with open('README.md', 'r') as readme:
    long_description = readme.read()

setup(
    name='walkmapper2',
    version='0.1.1',
    author='Keith Toh',
    author_email='ktprograms@gmail.com',
    description='A package for plotting and animating .gpx files',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://codeberg.org/ktprograms/walkmapper',
    packages=find_packages(include='walkmapper'),
    install_requires=[
        'gpxpy==1.5.0',
        'matplotlib==3.5.1',
        'numpy==1.22.1',
        'pandas==1.4.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
