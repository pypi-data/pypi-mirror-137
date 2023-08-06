import setuptools
setuptools.setup(
    name="Safety_line_project",
    version="0.0.1",                        
    author="Djeinaba",
    author_email="djeinaba.ba@insa.ueuromed.org",
    description="long description",
    long_description="python package for ML models",
    long_description_content_type="text/markdown",
    install_requires=[                      
        "json",
        "numpy",
        "sklearn"
                                                  
    ],                                             
    url="https://gitlab.com/Djeinaba_Doro/test_project",  
    packages=setuptools.find_packages(),
    classifiers=(                                 
        "Programming Language :: Python :: 3",    
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",   
    ),
)
