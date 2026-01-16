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
    from example_rdf.example_rdf.converters.examplefour_converter import ExampleFourConverter
    from example_rdf.example_rdf import default_ns, onto_ns
    print("Import successful!")
except ImportError as e:
    print(f"Import failed: {e}")
    print(f"Current path: {sys.path[:3]}")
    exit(1)
def test_example_four_converter():
    """Test ExampleFourConverter with its own graph."""
    print("=== Testing ExampleFourConverter (Separate Graph) ===")

    # Create a new RDF graph for this test
    g = rdflib.Graph()
    g.bind("", default_ns)
    g.bind("onto", onto_ns)

    # No need to pass a graph - it creates its own
    example_four_converter = ExampleFourConverter()
    csv_file = "c:/Users/elham.nourghassemi/Documents/GitHub/CSV-Semantic-Converter/CSVToRDF/InputData/examplefour.csv"

    print(f"\nTesting with CSV file: {csv_file}")
    
    # Process functions
    count = example_four_converter.process_examplefour_csv(csv_file,target_exampletwo_id="1" ,target_examplefour_id="CODE1")
    
    print(f"Processed examplefour: {count}")
    print(f"Total triples: {example_four_converter.get_triples_count()}")

    # Save to separate file
    example_four_converter.save_graph("examplefour_CODE1.ttl")

    # Show some triples
    print("\n--- Sample function triples: ---")
    for i, (s, p, o) in enumerate(example_four_converter.get_graph()):
        if i < 10:
            print(f"{i+1}: {s} {p} {o}")
        else:
            break

def test_all_examplefour():
    """Test processing all examplefour."""
    print("\n\n=== Testing All examplefour ===")
    g = rdflib.Graph()
    g.bind("", default_ns)
    g.bind("onto", onto_ns)
    examplefour_converter = ExampleFourConverter()
    csv_file = "c:/Users/elham.nourghassemi/Documents/GitHub/CSV-Semantic-Converter/CSVToRDF/InputData/examplefour.csv"

    count = examplefour_converter.process_examplefour_csv(csv_file)

    print(f"Processed examplefour: {count}")
    print(f"Total triples: {examplefour_converter.get_triples_count()}")

    examplefour_converter.save_graph("all_examplefour.ttl")

if __name__ == "__main__":
    test_example_four_converter()
    test_all_examplefour()