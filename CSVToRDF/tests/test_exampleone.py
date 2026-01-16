import rdflib
import sys
import os

# Get the absolute path to the RDFMapping directory
current_file = os.path.abspath(__file__)
test_dir = os.path.dirname(current_file)           # tests directory
example_dir = os.path.dirname(test_dir)           # example_rdf directory
rdf_mapping_dir = os.path.dirname(example_dir)    # RDFMapping directory

print(f"Adding to path: {rdf_mapping_dir}")
sys.path.insert(0, rdf_mapping_dir)

# Verify the import works
try:
    from example_rdf.example_rdf.converters import ExampleOneConverter
    from example_rdf.example_rdf import default_ns, onto_ns
    print("Import successful!")
except ImportError as e:
    print(f"Import failed: {e}")
    print(f"Current path: {sys.path[:3]}")
    exit(1)

# Simple imports thanks to __init__.py
from example_rdf.example_rdf.converters import ExampleOneConverter
from example_rdf.example_rdf import default_ns, onto_ns

def test_exampleone_converter():
    # Create a temporary RDF graph
    g = rdflib.Graph()
    g.bind("", default_ns)
    g.bind("onto", onto_ns)


    # Create a ExampleOneConverter instance
    exampleone_converter = ExampleOneConverter(g)
    csv_file = "c:/Users/elham.nourghassemi/Documents/GitHub/CSV-Semantic-Converter/CSVToRDF/InputData/exampleone.csv"

    # Filter for specific example (ExampleOneID = "200010")
    count = exampleone_converter.process_exampleone_csv(csv_file, target_exampleone_id="1")
    
    # Save results
    output_file = "exampleone.ttl"
    g.serialize(destination=output_file, format='turtle')
    print(f"ExampleOne RDF saved to {output_file}")
    print(f"Total triples: {len(g)}")
    print(f"Processed examples: {count}")

if __name__ == "__main__":
    test_exampleone_converter()