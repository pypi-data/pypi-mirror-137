from setuptools import setup, find_packages

VERSION = '1.0.3' 
DESCRIPTION = 'GEDSpy'
LONG_DESCRIPTION = 'GEDSpy is the python library for gene list enrichment with genes ontology, pathways and potential drugs. Package description  on https://github.com/jkubis96/GEDSpy'

# Setting up
setup(
        name="GEDSpy", 
        version=VERSION,
        author="Jakub Kubis",
        author_email="jbiosystem@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['requests', 'bioservices', 'pandas', 'tqdm', 'seaborn', 'matplotlib', 'scipy', 'networkx', 'pyvis'],       
        keywords=['python', 'GO', 'pathways', 'drug', 'gene ontology'],
        license = 'MIT',
        classifiers = [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX :: Linux",
        ],
        python_requires='>=3.6',
)


