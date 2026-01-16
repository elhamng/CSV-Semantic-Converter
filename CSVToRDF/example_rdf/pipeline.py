import os
import sys
from rdflib import Graph
from datetime import date,datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from .converters import ( 
    ExampleOneConverter,
    ExampleTwoConverter,
    ExampleThreeConverter,
    ExampleFourConverter
    )

from .namespaces import (
    default_ns, 
    onto_ns    
)

from .temporal_utils import DayInstanceGenerator

class EXAMPLERDFProcessor:
    """Main class to process Example CSV data into RDF using various converters."""
    def __init__(self, csv_directory, output_directory):
        """Initialize the pipline.
        
        Args:
            csv_directory (str): Path to the directory containing CSV files.
            output_directory (str): Path to the directory to save RDF output.
        """

        self.csv_directory = csv_directory
        self.output_directory = output_directory
        # Ensure output directory exists
        os.makedirs(self.output_directory, exist_ok=True)
        #CSV files
        self.csv_files = {
            "exampleone": os.path.join(self.csv_directory, "exampleone.csv"),
            "exampletwo": os.path.join(self.csv_directory, "exampletwo.csv"),
            "examplethree": os.path.join(self.csv_directory, "examplethree.csv"),
            "examplefour": os.path.join(self.csv_directory, "examplefour.csv"),
            }
        #output file paths
        self.output_files = {
            #"exampleone": os.path.join(self.output_directory, "exampleone.ttl"),
            #"exampletwo": os.path.join(self.output_directory, "exampletwo.ttl"),
            #"examplethree": os.path.join(self.output_directory, "examplethree.ttl"),
            #"examplefour": os.path.join(self.output_directory, "examplefour.ttl"),
            "example_core": os.path.join(self.output_directory, "example_core.ttl"),
            "category": os.path.join(self.output_directory, "category.ttl"),
            "temporal": os.path.join(self.output_directory, "example_days.ttl")
        }



    def process_example_core(self, target_exampleone_id=None, target_exampletwo_id=None):
        """Run the core Example RDF conversion pipeline."""
        # Create main RDF graph for core data
        core_graph = Graph()
        core_graph.bind("", default_ns)
        core_graph.bind("onto", onto_ns)
        
        total_triples = 0
        
        # 1. Process Persons
        if os.path.exists(self.csv_files['exampleone']):
            print("\nProcessing Example One...")
            exampleone_converter = ExampleOneConverter(core_graph)
            exampleone_count = exampleone_converter.process_exampleone_csv(
                self.csv_files['exampleone'],
                target_exampleone_id=target_exampleone_id
            )
            print(f"Processed {exampleone_count} Example One records")
        else:
            print("Example One CSV not found")

        # 2. Process Example Two
        if os.path.exists(self.csv_files['exampletwo']):
            print("\nProcessing Example Two...")
            exampletwo_converter = ExampleTwoConverter(core_graph)
            exampletwo_count = exampletwo_converter.process_exampletwo_csv(
                self.csv_files['exampletwo'],
                target_exampletwo_id=target_exampletwo_id,
                target_exampleone_id=target_exampleone_id
            )
            print(f"Processed {exampletwo_count} Example Two records")
        else:
            print("Example Two CSV not found")

        # 3. Process Example Three
        if os.path.exists(self.csv_files['examplethree']):
            print("\nProcessing Example Three...")
            examplethree_converter = ExampleThreeConverter(core_graph)
            examplethree_count = examplethree_converter.process_example_three_csv(
                self.csv_files['examplethree'],
                target_exampletwo_id=target_exampletwo_id,
                target_exampleone_id=target_exampleone_id
            )
            print(f"Processed {examplethree_count} Example Three records")
        else:
            print("Example Three CSV not found")

        # Save core data
        total_triples = len(core_graph)
        print(f"\nSaving core data...")
        core_graph.serialize(destination=self.output_files['example_core'], format='turtle')
        print(f"Core RDF saved to: {self.output_files['example_core']}")
        print(f"Total core triples: {total_triples}")
        
        return total_triples

    def process_functions(self, target_exampletwo_id=None, target_examplefour_id=None):
        """Run the function pipeline: Function data only.
        
        Args:
            target_examplefour_id (str, optional): Filter for specific function
        """
        print("\n" + "=" * 60)
        print("STARTING FUNCTION PIPELINE")
        print("=" * 60)
        
        if os.path.exists(self.csv_files['examplefour']):
            print("\nProcessing Functions...")
            examplefour_converter = ExampleFourConverter()  # Own graph
            function_count = examplefour_converter.process_examplefour_csv(
                self.csv_files['examplefour'],
                target_exampletwo_id=target_exampletwo_id,
                target_examplefour_id=target_examplefour_id
            )
            
            # Save function data
            examplefour_converter.save_graph(self.output_files['category'])
            function_triples = examplefour_converter.get_triples_count()

            print(f"Function RDF saved to: {self.output_files['category']}")
            print(f"Total function triples: {function_triples}")
            return function_triples
        else:
            print("Function CSV not found")
            return 0

    
    def generate_dagen(self, start_year, end_year):
        """Generate day instances for a given date range."""
        print("\n" + "=" * 60)
        print("STARTING DAY INSTANCE GENERATION")
        print("=" * 60)
        
        
        day_generator = DayInstanceGenerator()
        count = day_generator.generate_day_instances(start_year, end_year)
        
        day_generator.serialize_graph(self.output_files['temporal'])
        triple_count = day_generator.get_triples_count()
        print(f"Day instances generated: {count}")
        print(f"Day instances RDF saved to: {self.output_files['temporal']}")
        print(f"Total temporal triples: {triple_count}")
        return triple_count
    
    def run_full_pipeline(self, target_exampleone_id=None, target_exampletwo_id=None, 
                            target_examplefour_id=None):
        """Run the complete pipeline: All converters.
        
        Args:
            target_exampleone_id (str, optional): Filter for specific Example One
            target_exampletwo_id (str, optional): Filter for specific Example Two
            target_examplefour_id (str, optional): Filter for specific Example Four
            
        """
        start_time = datetime.now()
        print("=" * 60)
        print("STARTING FULL EXAMPLE RDF PIPELINE")
        print(f"Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Run all pipelines
        core_triples = self.process_example_core(target_exampleone_id, target_exampletwo_id)
        function_triples = self.process_functions(target_exampletwo_id, target_examplefour_id)

        # Final summary
        end_time = datetime.now()
        duration = end_time - start_time
        total_triples = core_triples + function_triples 
        
        print("\n" + "=" * 60)
        print("PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print(f"Completed at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Duration: {duration}")
        print(f"Total triples generated: {total_triples}")
        print(f"Core data triples: {core_triples}")
        print(f"Function triples: {function_triples}")
        print("\nOutput files:")
        print(f"  Core: {self.output_files['example_core']}")
        print(f"  Function: {self.output_files['category']}")
        print("=" * 60)
        return total_triples

    def run_full_pipeline_with_temporal(self, start_date=2020, end_date=2025,
                                    target_exampleone_id=None, target_exampletwo_id=None, 
                                    target_examplefour_id=None):
        """Run the complete pipeline including day instance generation.
        
        Args:
            start_date (date): Start date for day instance generation
            end_date (date): End date for day instance generation
            target_exampleone_id (str, optional): Filter for specific Example One
            target_exampletwo_id (str, optional): Filter for specific Example Two
            target_examplefour_id (str, optional): Filter for specific Example Four
        """

        print("=" * 60)
        print("STARTING FULL EXAMPLE RDF PIPELINE WITH TEMPORAL DATA")
        print(f"Temporal period: {start_date} to {end_date}")
        print("=" * 60)
        all_pipelines = self.run_full_pipeline(
            target_exampleone_id=target_exampleone_id,
            target_exampletwo_id=target_exampletwo_id,
            target_examplefour_id=target_examplefour_id
        )

        # Generate day instances
        temporal =  self.generate_dagen(start_date, end_date)

        total_triples = all_pipelines + temporal
        print(f"\nTotal triples including temporal data: {total_triples}")

def main():
    """Main pipeline execution."""
    # Configuration
    csv_directory = "c:/example-python/EXAMPLE/inputdata"
    output_directory = "c:/example-python/EXAMPLE/Output"

    # Create pipeline
    pipeline = EXAMPLERDFProcessor(csv_directory, output_directory)
    
    # Example 1: Run full pipeline without filters
    print("Option 1: Full Pipeline (All data)")
    pipeline.run_full_pipeline()
    
    # Example 2: Run with specific filters
    # print("Option 2: Filtered Pipeline")
    # pipeline.run_full_pipeline(
    #     target_exampleone_id="200010",
    #     target_exampletwo_id="200010_1",
    #     target_examplefour_id="GOV1040"
    #     
    # )
    
    # Example 3: Run individual pipelines
    # print("Option 3: Individual Pipelines")
    # pipeline.process_example_core()
    # pipeline.process_functions()

    # Example 4: Generate day instances for a specific range
    #print("Option 4: Generate Day Instances")
    #pipeline.run_full_pipeline_with_temporal()



if __name__ == "__main__":
    main()


