import setuptools

# Setting up
setuptools.setup(
        name="micnet", 
        version="1.0.0",
        author="Natalia Favila, David Madrigal-Trejo, Daniel Legorreta",
        author_email="natalia.favila.v@gmail.com",
        description="Toolbox for the visualization and analysis of microbial datasets",
        long_description=open('README.md').read(),
        long_description_content_type='text/markdown',
	install_requires=[],
        classifiers= [
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
        ],
	include_package_data=True,
	packages=setuptools.find_packages(),
	package_data={'': ['data/*.txt']},
)