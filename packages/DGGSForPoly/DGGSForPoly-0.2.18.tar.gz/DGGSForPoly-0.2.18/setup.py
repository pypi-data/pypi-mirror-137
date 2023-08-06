import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DGGSForPoly",
    version="0.2.18",
    author="Ross Petridis",
    author_email="ross.petridis@csiro.au",
    description="This package finds the rHEALPIX dggs cells for Polygons using the rhgealpix dggs engine.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CSIRO-enviro-informatics/DGGSForPoly",
    project_urls={
        "Bug Tracker": "https://github.com/CSIRO-enviro-informatics/DGGSForPoly/issues",
    },
       
    packages=setuptools.find_packages(),

    install_requires = [ 
        'Shapely',
        'rhealpixdggs'
    ],
        
)
