import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='specivar',
    version='0.0.6',
    author='Anthony Aylward',
    author_email='aaylward@salk.edu',
    description='Filter VCF to variants that are specific to a sample group',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/salk-tm/specivar',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=['pysam'],
    entry_points={
        'console_scripts': ['specivar=specivar.specivar:main']
    },
    include_package_data=True
)
