import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pysmoove_summary',
    version='0.0.1',
    author='Anthony Aylward',
    author_email='aaylward@salk.edu',
    description='Summarize pysmoove SV calling VCF results in a BED-like format',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/salk-tm/pysmoove_summary',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=['pysam', 'pysmoove'],
    entry_points={
        'console_scripts': ['pysmoove-summary=pysmoove_summary.pysmoove_summary:main']
    },
    include_package_data=True
)
