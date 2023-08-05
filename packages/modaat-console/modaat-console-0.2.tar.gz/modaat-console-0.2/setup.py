from setuptools import setup

# reading long description from file
with open('README.md') as file:
    long_description = file.read()


# specify requirements of your package here
REQUIREMENTS = ["requests>=2.27.1", "erddapy", "pandas>=1.4"]

# https://pypi.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Developers',
    'Topic :: Internet',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.10',
    'Environment :: Console',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Topic :: Scientific/Engineering :: Atmospheric Science'
]

# calling the setup function
setup(name='modaat-console',
      version='0.2',
      description='Connect to an OPeNDAP service (ERDDAP) and query data and metadata through a simple console menu.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/CEN-ULaval/modaat',
      author='Etienne Godin',
      author_email='etienne.godin@cen.ulaval.ca',
      license='MIT',
      packages=["modaat_console"],
      entry_points={"console_scripts": ['modaat_console = modaat_console.modaat:main']},
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      keywords='erddap MODAAT OPeNDAP DAP CCADI CEN',
      python_requires='>=3.10',
      )
