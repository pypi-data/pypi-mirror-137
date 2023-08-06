import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='heppyness',
    license='HEP license, based on MIT license',
    version='1.5.2',
    author='Stefan Richter',
    author_email='stefan.richter@cern.ch',
    maintainer='Stefan Richter',
    maintainer_email='stefan.richter@cern.ch',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.cern.ch/strichte/heppy',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Physics',
    ],
    install_requires=[
        'matplotlib',
        'numpy',
        'root-numpy',
        'uproot',
        'uproot-methods',
        'pandas',
        'pyyaml',
    ],
    python_requires='>=3.6',
)
