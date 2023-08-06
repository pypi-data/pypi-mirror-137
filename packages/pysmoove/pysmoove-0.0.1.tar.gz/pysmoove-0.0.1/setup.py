import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pysmoove',
    version='0.0.1',
    author='Anthony Aylward',
    author_email='aaylward@salk.edu',
    description='Execute the population-level SV calling workflow for smoove',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/salk-tm/pysmoove',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[],
    entry_points={
        'console_scripts': ['pysmoove=pysmoove.pysmoove:main']
    },
    include_package_data=True
)
