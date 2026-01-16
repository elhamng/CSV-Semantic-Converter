import os
import sys
import argparse

# Add the RDFMapping directory to Python path FIRST
rdf_mapping_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, rdf_mapping_dir)

# NOW import after path is set
from example_rdf.example_rdf.pipeline import EXAMPLERDFProcessor

class EXAMPLECLI:
    """Command-line interface for EXAMPLE RDF processing."""

    @staticmethod
    def parse_args():
        """Parse command-line arguments. """
        parser = argparse.ArgumentParser(description="EXAMPLE RDF Pipeline - Convert EXAMPLE CSVs to RDF triples.")

        parser.add_argument('--csv-dir', type=str, default="c:/Users/elham.nourghassemi/Documents/GitHub/CSV-Semantic-Converter/CSVToRDF/InputData",
                            help='Directory containing EXAMPLE CSV files.')

        parser.add_argument('--output-dir', type=str, default="c:/Users/elham.nourghassemi/Documents/GitHub/CSV-Semantic-Converter/CSVToRDF/OutputData",
                            help='Directory to save the output RDF files.')
        


        return parser.parse_args()
    @staticmethod
    def main():
        """Main method to run the EXAMPLE RDF processing pipeline."""
        #csv_directory = "c:/yourdirectory/EXAMPLE/inputdata"
        #output_directory = "c:/yourdirectory/EXAMPLE/CLI_Output"
        args = EXAMPLECLI.parse_args()
        csv_directory = args.csv_dir
        output_directory = args.output_dir


        print("Starting EXAMPLE RDF CLI...")
        print(f"CSV Directory: {csv_directory}")
        print(f"Output Directory: {output_directory}")

        if not os.path.isdir(csv_directory):
            print(f"Error: CSV directory '{csv_directory}' does not exist.")
            return 1
        
        try:
            # Create output directory if it doesn't exist
            os.makedirs(output_directory, exist_ok=True)
            
            # Create pipeline
            pipeline = EXAMPLERDFProcessor(csv_directory, output_directory)

            # Run full pipeline
            print("\n" + "="*60)
            print("STARTING EXAMPLE RDF PIPELINE VIA CLI")
            print("="*60)
            
            triples = pipeline.run_full_pipeline()

            print(f"\nEXAMPLE RDF processing completed via CLI.")
            print(f"Files saved to: {output_directory}")
            print(f"Total triples: {triples}")
            
        except Exception as e:
            print(f"Pipeline Error: {e}")
            import traceback
            traceback.print_exc()
            return 1
        
        return 0

def main():
    """Entry point for the CLI when installed as a package."""
    import sys
    result = EXAMPLECLI.main()
    sys.exit(result)

if __name__ == '__main__':
    result = EXAMPLECLI.main()
    sys.exit(result)