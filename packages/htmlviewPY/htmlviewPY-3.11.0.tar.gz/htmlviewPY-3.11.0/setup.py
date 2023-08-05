from setuptools import setup, find_packages

VERSION = '3.11.0' 
DESCRIPTION = 'View and print the HTML of websites!'
LONG_DESCRIPTION = 'Useful for webscraping. This module allows you to view the html from pages, in a single line!'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="htmlviewPY", 
        version=VERSION,
        author="Daniel Duchouquette",
        author_email="<danpersonguything@email.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'Simple', 'HTML', 'view', 'webscraping'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)