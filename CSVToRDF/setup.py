from setuptools import setup, find_packages

setup(
    name="example-rdf",
    version="0.1.0",
    description="Convert Example CSV data to RDF using ontology",
    author="Elham Nour Ghassemi",
    packages=find_packages(),
    install_requires=[
        "rdflib",
        "pandas",
    ],
    entry_points={
        "console_scripts": [
            "example-rdf=example_rdf.cli.example_rdf_cli:main",
        ]
    },
    include_package_data=True,
    python_requires='>=3.7',
)
