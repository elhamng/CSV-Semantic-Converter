import os
import sys
import rdflib

current_file = os.path.abspath(__file__)
tests_dir = os.path.dirname(current_file)           # tests directory
example_dir = os.path.dirname(tests_dir)           # example_rdf directory
rdf_mapping_dir = os.path.dirname(example_dir)     # RDFMapping directory

print(f"Adding to path: {rdf_mapping_dir}")
sys.path.insert(0, rdf_mapping_dir)

# Verify the import works
try:
    from example_rdf.example_rdf.converters.exampletwo_converter import ExampleTwoConverter
    from example_rdf.example_rdf import default_ns, onto_ns
    print("Import successful!")
except ImportError as e:
    print(f"Import failed: {e}")
    print(f"Current path: {sys.path[:3]}")
    exit(1)

def test_exampletwo_converter():
    # Create a temporary RDF graph
    g = rdflib.Graph()
    g.bind("", default_ns)
    g.bind("onto", onto_ns)

    # Create a ExampleTwoConverter instance
    exampletwo_converter = ExampleTwoConverter(g)
    csv_file = "c:/Users/elham.nourghassemi/Documents/GitHub/CSV-Semantic-Converter/CSVToRDF/InputData/exampletwo.csv"

    # Test 1: Filter for specific contract and person
    print("\n--- Test 1: Filter for ExampleTwoID='1' and ExampleOneID='2' ---")
    count = exampletwo_converter.process_exampletwo_csv(
        csv_file,
        target_exampletwo_id="1",
        target_exampleone_id="2"
    )
    
    print(f"Processed exampletwo: {count}")
    print(f"Total triples: {len(g)}")
    
    # Save results
    output_file = "exampletwo.ttl"
    g.serialize(destination=output_file, format='turtle')
    print(f"ExampleTwo RDF saved to {output_file}")

def test_all_exampletwo():
    """Test processing all exampletwo without filters."""
    print("\n\n=== Testing All ExampleTwo (No Filter) ===")

    # Create new graph
    g = rdflib.Graph()
    g.bind("", default_ns)
    g.bind("onto", onto_ns)

    exampletwo_converter = ExampleTwoConverter(g)
    csv_file = "c:/Users/elham.nourghassemi/Documents/GitHub/CSV-Semantic-Converter/CSVToRDF/InputData/exampletwo.csv"

    # Process all exampletwo
    count = exampletwo_converter.process_exampletwo_csv(csv_file)

    print(f"Processed exampletwo: {count}")
    print(f"Total triples: {len(g)}")
    
    # Save results
    output_file = "all_exampletwo.ttl"
    g.serialize(destination=output_file, format='turtle')
    print(f"All exampletwo RDF saved to {output_file}")

if __name__ == "__main__":
    test_exampletwo_converter()
    test_all_exampletwo()