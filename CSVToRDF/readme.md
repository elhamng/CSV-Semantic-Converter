# CSV Semantic Converter

Convert CSV data into RDF (Turtle/TTL) using a shared ontology schema defined with Owlready2. Includes reusable CLI, converters, and tests.

## Library Structure

```
CSV-Semantic-Converter/
├─ ontology/
│  ├─ onto.py
│  ├─ main.py
│  └─ classes/
│     ├─ author.py
│     ├─ book.py
│     └─ publisher.py
└─ CSVToRDF/
   ├─ example_rdf/
   │  ├─ __init__.py
   │  ├─ cli/
   │  │  ├─ __init__.py
   │  │  └─ example_rdf_cli.py
   │  ├─ example_rdf/converters/
   │  │  ├─ __init__.py
   │  │  ├─ exampletwo_converter.py
   │  │  ├─ examplethree_converter.py
   │  │  └─ examplefour_converter.py
   |  |--example_rdf
   |     |--pipeline.py
   |  |  |--graph_manager.py
   |  |  |--namespaces.py
   |  |  |--utils.py
   |  |  |--temporal_utils.py
   │  ├─ tests/
   │  │  ├─ __init__.py
   │  │  └─ test_cli.py
   │  └─ 
   ├─ InputData/
   ├─ OutputData/
   ├─ OutputData-cli/
   └─ Output/
```

## Library Pattern (Imports and Testability)

- Use a single package level: `example_rdf` (avoid nested `example_rdf.example_rdf`).
- Place reusable code under `example_rdf/` and expose stable imports:
  - Converters: `from example_rdf.converters.exampletwo_converter import ExampleTwoConverter`
  - Namespaces: `from example_rdf import default_ns, onto_ns`
  - CLI: `from example_rdf.cli.example_rdf_cli import EXAMPLECLI`
  - Pipeline: `from example_rdf.pipeline import EXAMPLERDFProcessor`

- Ensure `__init__.py` exists in:
  - `example_rdf/`, `example_rdf/converters/`, `example_rdf/cli/`, `example_rdf/tests/`

- Do not modify `sys.path` inside library modules (CLI/converters/pipeline). Tests or the runner should add the project root.


# RDF Converter

A Python package for converting CSV data to RDF/TTL format using the ontology.

## Features

- Convert EXAMPLE CSV files to RDF triples
- Support for multiple data types: exampleone, exampletwo, examplethree, example four, and ...
- Command-line interface for easy automation
- Flexible filtering options for targeted processing
- Temporal data generation for day instances
- Multiple output formats (TTL files)

## Installation

### From Source

```bash
# Clone the repository
cd c:\directory_to_your_lib\CSVToRDF

# Install in development mode
pip install -e .

# Or install normally
pip install .
```

### Development Installation

```bash
# Install with development dependencies
pip install -e ".[dev]"
```

## Usage

### Command Line Interface

After installation, you can use the `example-rdf` command:

```bash
# Basic usage with default paths
example-rdf

# Custom input and output directories
example-rdf --csv-dir "path\to\csv\files" --output-dir "path\to\output"

# Get help
example-rdf --help
```

### Python API

```python
from example_rdf.example_rdf.pipeline import EXAMPLERDFProcessor

# Create processor
processor = EXAMPLERDFProcessor(
    csv_directory="path/to/csv/files",
    output_directory="path/to/output"
)

# Run full pipeline
total_triples = processor.run_full_pipeline()

# Run with filters
processor.run_full_pipeline(
    target_exampleone_id="2",
    target_exampletwo_id="2"
)
```

## Requirements

- Python 3.8+
- rdflib>=6.0.0
- pandas>=1.3.0
- python-dateutil>=2.8.0

## Running Tests

- From CSVToRDF:
  - python -m pytest example_rdf\tests\test_cli.py -v
  - python -m pytest example_rdf\tests\test_exampletwo.py -v

If pytest can’t find modules, run from CSVToRDF or add project root to `sys.path` as shown above.


## Input Files

The converter expects these CSV files in your input directory:
- `exampleone.csv`
- `exampletwo.csv`
- `examplethree.csv`
- `examplefour.csv`

## Output Files

The converter generates these RDF files:
- `example_core.ttl` - Core example data (one, three)
- `category.ttl` - Category data
- `example_dagen.ttl` - Temporal day instances (when using temporal pipeline)

## Development

### Running Tests

```bash
pytest example_rdf/tests/
```

### Code Formatting

```bash
black example_rdf/
```

### Type Checking

```bash
mypy example_rdf/
```




## Project Structure

- ontology/
  - onto.py: Shared ontology namespace
  - classes/: Author, Book, Publisher classes and properties
  - main.py: Central registries and save/get helpers
- CSVToRDF/
  - example_rdf/
    - cli/example_rdf_cli.py: Reusable CLI to run the pipeline
    - converters/: CSV converters (ExampleTwo/Three/Four…)
    - tests/test_cli.py: Pytest for CLI args
  - InputData/: CSV files to convert
  - OutputData/: TTL outputs
  - OutputData-cli/: TTL outputs created by CLI

## Requirements

- Python 3.10+
- pip install:
  - owlready2
  - rdflib
  - pandas
  - pytest

## Setup

- Open terminal in VS Code.
- Windows commands:
  - Create venv: python -m venv .venv
  - Activate: .\.venv\Scripts\activate
  - Install: pip install -r requirements.txt
    - Or: pip install owlready2 rdflib pandas pytest

## Ontology Schema

- Shared ontology in `ontology/onto.py`
- Classes and properties split into files under `ontology/classes/`
- Central registry and save helpers in `ontology/main.py`
  - get_ontology_schema(): returns dict of classes/properties/ontology
  - save_ontology(file_path): saves schema (no instances)

## Running the CLI

- CLI defines defaults pointing to InputData and OutputData.
- Run from CSVToRDF folder:
  - python -m example_rdf.cli.example_rdf_cli
- Override paths:
  - python -m example_rdf.cli.example_rdf_cli --csv-dir "C:\path\to\InputData" --output-dir "C:\path\to\OutputData"

The CLI constructs and runs the pipeline (EXAMPLERDFProcessor) and writes TTL files into the output directory.

## Running Tests

- From CSVToRDF folder:
  - python -m pytest example_rdf\tests\test_cli.py -v
- If pytest cannot find the module, ensure:
  - example_rdf, example_rdf/cli, and example_rdf/tests have __init__.py
  - You run pytest from CSVToRDF (project root for the package)

## Common Issues

- ImportError: attempted relative import with no known parent package
  - Run modules from the project root (CSVToRDF) or use absolute imports (e.g., `from ontology.onto import onto`).
- FileNotFoundError for CSV
  - Use full Windows paths (raw strings: r"C:\...") or place CSVs in CSVToRDF\InputData.
- AssertionError in test_cli
  - Ensure CLI defaults match test expectations: InputData and OutputData (case-sensitive on assertions).

## Example: Programmatic Conversion

You can use the registry and a converter to generate TTL:

```python
from ontology.main import get_ontology_schema, save_ontology
from rdflib import Graph

schema = get_ontology_schema()
g = Graph()
# Add triples based on your converters and mapping…
g.serialize(destination="CSVToRDF\\OutputData\\example_core.ttl", format="turtle")
```

## Outputs

- Core TTL examples are saved under:
  - CSVToRDF\OutputData\example_core.ttl
  - CSVToRDF\OutputData-cli\example_core.ttl

These contain instances linked via properties like `onto:hasPart`, `onto:isAbout`, and time instants using `time:Instant`.

## Contributing

- Keep imports absolute (avoid sys.path hacks inside library code).
- Expose parser via `EXAMPLECLI.build_parser()` and allow `main(argv=None)` for testability.
- Add tests under `example_rdf/tests` and run via pytest.

## License

This project is intended for internal use. Add a LICENSE if you plan to distribute.