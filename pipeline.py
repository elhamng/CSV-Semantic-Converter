import os
import sys
from rdflib import Graph, Namespace, RDF, RDFS, URIRef, Literal
from rdflib.namespace import FOAF, DC

from .Convereters import firstConverter, secondConverter

from .Namespaces import default_namespaces, SCHEMA, EXAMPLE

class RDFProcessor:
    def __init__(self, csv_directory=None, rdf_directory=None):

        """Initialize the RDFProcessor with optional CSV or RDF file."""
        self.csv_directory = csv_directory
        self.rdf_directory = rdf_directory
        os.makedirs(self.rdf_directory, exist_ok=True)

        # Generic csv files
        self.generic_csv_files = {
            "data1": os.path.join(self.csv_directory, "data1.csv"),
            "data2": os.path.join(self.csv_directory, "data2.csv"),
            "data3": os.path.join(self.csv_directory, "data3.csv"),
            "data4": os.path.join(self.csv_directory, "data4.csv"),
            "data5": os.path.join(self.csv_directory, "data5.csv")
        }

        # RDF files
        self.rdf_files = {
            "Main": os.path.join(self.rdf_directory, "RDF1.rdf"),
            "RDF2": os.path.join(self.rdf_directory, "RDF2.rdf"),
            "RDF3": os.path.join(self.rdf_directory, "RDF3.rdf")
        }

        


        def process_files(self, target_1_id=None,target_2_id=None):
            """Process CSV files and convert them to RDF format."""

            main_graph = Graph()
            for prefix, namespace in default_namespaces.items():
                main_graph.bind(prefix, namespace)
            if os.path.exists(self.csv_files["data1"]):
                print("Processing data1.csv...")
                firstconverter = firstConverter(main_graph)
                first_count = firstconverter.process_csv_to_rdf(self.csv_files["data1"],                                              
                                                                target_1_id, target_2_id)
                print(f"processed {first_count} triples from data1.csv")
            else:
                print("data1.csv not found, skipping.")
            if os.path.exists(self.csv_files["data2"]):
                print("Processing data2.csv...")
                secondconverter = secondConverter(main_graph)
                second_count = secondconverter.process_csv_to_rdf(self.csv_files["data2"],
                                                                    target_1_id, target_2_id)
                print(f"processed {second_count} triples from data2.csv")
            else:
                print("data2.csv not found, skipping.")
            if os.path.exists(self.csv_files["data3"]):
                print("Processing data3.csv...")
                secondconverter = secondConverter(main_graph)
                second_count = secondconverter.process_csv_to_rdf(self.csv_files["data3"],
                                                                    target_1_id, target_2_id)
                print(f"processed {second_count} triples from data3.csv")
            else:
                print("data3.csv not found, skipping.")

            total_triples = len(main_graph)
            print(f"Total triples in the main graph: {total_triples}")
            # Serialize the main graph to RDF files
            main_graph.serialize(destination=self.rdf_files["Main"], format="turtle")

            print(f"Serialized main graph to {self.rdf_files['Main']}")

            return total_triples
        
        def process_additional_files(self,target_1_id=None,target_2_id=None):
            """Process additional CSV files and convert them to RDF format."""
            if os.path.exists(self.csv_files["data4"]):
                print("Processing data4.csv...")
                additional_graph = Graph()
                for prefix, namespace in default_namespaces.items():
                    additional_graph.bind(prefix, namespace)
                secondconverter = secondConverter(additional_graph)
                count = secondconverter.process_csv_to_rdf(self.csv_files["data4"])
                print(f"processed {count} triples from data4.csv")
                additional_graph.serialize(destination=self.rdf_files["RDF2"], format="turtle")
                print(f"Serialized additional graph to {self.rdf_files['RDF2']}")
            else:
                print("data4.csv not found, skipping.")

            if os.path.exists(self.csv_files["data5"]):
                print("Processing data5.csv...")
                    
                roleconverter = secondConverter() # Use a new graph inside the converter
                count = roleconverter.process_csv_to_rdf(self.csv_files["data5"])
                print(f"processed {count} triples from data5.csv")
                roleconverter.serialize(destination=self.rdf_files["RDF3"], format="turtle")
                print(f"Serialized additional graph to {self.rdf_files['RDF3']}")
            else:
                print("data5.csv not found, skipping.")

            print("Additional processing completed.")