import sys
import os

# Add the RDFMapping directory to Python path
rdf_mapping_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, rdf_mapping_dir)

from example_rdf.example_rdf.pipeline import EXAMPLERDFProcessor

def test_filtered_pipeline():
    """Test pipeline with filters for specific id."""
    print("=== Testing Filtered Pipeline ===")
    csv_directory = "c:/Users/elham.nourghassemi/Documents/GitHub/CSV-Semantic-Converter/CSVToRDF/InputData"
    output_directory = "c:/Users/elham.nourghassemi/Documents/GitHub/CSV-Semantic-Converter/CSVToRDF/OutputData"

    # Create pipeline
    pipeline = EXAMPLERDFProcessor(csv_directory, output_directory)
    
    # Run with filters for testing
    #pipeline.run_full_pipeline(
     #   target_exampleone_id="1",
      #  target_exampletwo_id="2",
       # target_examplefour_id="CODE1"
    #)
    pipeline.run_full_pipeline()

def test_core_only():
    """Test only the core pipeline."""
    print("=== Testing Core Pipeline Only ===")

    csv_directory = "c:/Users/elham.nourghassemi/Documents/GitHub/CSV-Semantic-Converter/CSVToRDF/InputData"
    output_directory = "c:/Users/elham.nourghassemi/Documents/GitHub/CSV-Semantic-Converter/CSVToRDF/OutputData"

    pipeline = EXAMPLERDFProcessor(csv_directory, output_directory)
    pipeline.process_example_core(target_exampleone_id="1", target_exampletwo_id="1")
    #pipeline.process_example_core()

if __name__ == "__main__":
    #test_filtered_pipeline()
    test_core_only()