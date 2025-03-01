from setuptools import setup

setup(
    name='esupy',
    version='0.4.0',
    packages=['esupy'],
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=['requests>=2.22.0',
                      'appdirs>=1.4.3',
                      'pandas>=1.1.0',
                      'pyarrow>=4.0.0',
                      'pyyaml>=5.3',
                      'numpy>=1.20.1',
                      'boto3>=1.23.0',
                      ],
    extras_require={"urban_rural": ['geopandas>=0.13.2',
                                    'shapely>=2.0.1'],
                    "bib": ['olca_schema>=0.0.11',
                            'bibtexparser>=1.2']},
    url='http://github.com/usepa/esupy',
    license='CC0',
    author='Wesley Ingwersen',
    author_email='ingwersen.wesley@epa.gov',
    description='Common objects for USEPA LCA ecosystem tools'
)
