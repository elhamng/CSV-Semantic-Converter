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
    from example_rdf.example_rdf.converters.examplethree_converter import ExampleThreeConverter
    from example_rdf.example_rdf import default_ns, onto_ns
    print("Import successful!")
except ImportError as e:
    print(f"Import failed: {e}")
    print(f"Current path: {sys.path[:3]}")
    exit(1)

def test_examplethree_converter():
    # Create a temporary RDF graph
    g = rdflib.Graph()
    g.bind("", default_ns)
    g.bind("onto", onto_ns)


    # Create a ExampleThreeConverter instance
    examplethree_converter = ExampleThreeConverter(g)
    csv_file = "c:/Users/elham.nourghassemi/Documents/GitHub/CSV-Semantic-Converter/CSVToRDF/InputData/examplethree.csv"

    # Test 1: Filter for specific exampleoneId and exampletwoId
    print("\n--- Test 1: Filter for exampleoneId='1' and exampletwoId='1' ---")
    count = examplethree_converter.process_example_three_csv(
        csv_file, 
        target_exampletwo_id='1', 
        target_exampleone_id='1'
    )

    print(f"Processed examplethree: {count}")
    print(f"Total triples: {len(g)}")
    
    # Save results
    output_file = "examplethree.ttl"
    g.serialize(destination=output_file, format='turtle')
    print(f"ExampleThree RDF saved to {output_file}")

def test_all_examplethree():
    """Test processing all examplethree without filters."""
    print("\n\n=== Testing All ExampleThree (No Filter) ===")

    # Create new graph
    g = rdflib.Graph()
    g.bind("", default_ns)
    g.bind("onto", onto_ns)

    examplethree_converter = ExampleThreeConverter(g)
    csv_file = "c:/Users/elham.nourghassemi/Documents/GitHub/CSV-Semantic-Converter/CSVToRDF/InputData/examplethree.csv"

    # Process all examplethree
    count = examplethree_converter.process_example_three_csv(csv_file)

    print(f"Processed examplethree: {count}")
    print(f"Total triples: {len(g)}")
    
    # Save results
    output_file = "all_examplethree.ttl"
    g.serialize(destination=output_file, format='turtle')
    print(f"All examplethree RDF saved to {output_file}")

if __name__ == "__main__":
    test_examplethree_converter()
    test_all_examplethree()