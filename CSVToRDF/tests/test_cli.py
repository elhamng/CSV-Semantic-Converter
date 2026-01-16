import pytest
import os
import sys
current_file = os.path.abspath(__file__)
tests_dir = os.path.dirname(current_file)           # tests directory
example_dir = os.path.dirname(tests_dir)           # example_rdf directory
rdf_mapping_dir = os.path.dirname(example_dir)     # RDFMapping directory

print(f"Adding to path: {rdf_mapping_dir}")
sys.path.insert(0, rdf_mapping_dir)
# Verify the import works
try:
    from example_rdf.cli.example_rdf_cli import EXAMPLECLI
    print("Import successful!")
except ImportError as e:
    print(f"Import failed: {e}")
    print(f"Current path: {sys.path[:3]}")
    exit(1)

def test_parse_args_defaults(monkeypatch):
    """Test that default arguments are parsed correctly."""
    monkeypatch.setattr('sys.argv', ['example-rdf'])
    args = EXAMPLECLI.parse_args()
    assert args.csv_dir == "c:/Users/elham.nourghassemi/Documents/GitHub/CSV-Semantic-Converter/CSVToRDF/InputData"
    assert args.output_dir == "c:/Users/elham.nourghassemi/Documents/GitHub/CSV-Semantic-Converter/CSVToRDF/OutputData"