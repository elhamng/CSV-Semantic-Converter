import csv
from rdflib import Graph, RDF, RDFS, XSD, Literal
from ..namespaces import default_ns, onto_ns
from ..utils import is_bad_id, is_blank, safe_get_value, create_uri,normalize_id

class ExampleFourConverter:
    """ Converter class for processing ExampleFour CSV data into RDF. It save in seperate graph. """

    def __init__(self, graph=None):
        """Initialize with an RDF graph."""
        if graph is None:
            self.graph = Graph()
        else:    
            self.graph = graph

        # Bind namespaces    
        self.graph.bind("", default_ns)
        self.graph.bind("onto", onto_ns)

    def process_examplefour_csv(self, csv_file_path,target_exampletwo_id=None ,target_examplefour_id=None):
            """
            Process ExampleFour CSV to classify things into categories.
            adds categories to the RDF graph based on 'yes or not' column.
            
            Args:
                    csv_file_path (str): Path to the  CSV file
                    target_exampletwo_id (str, optional): Filter for specific example two (e.g., "1")
                    target_examplefour_id (str, optional): Filter for specific example four (e.g., "code123")
            """
            print(f"Processing examplefour from: {csv_file_path}")
            if target_exampletwo_id:
                print(f"  → Filtering for ExampleTwoID: {target_exampletwo_id}")
            if target_examplefour_id:
                print(f"  → Filtering for ExampleFourID: {target_examplefour_id}")

            category_count = 0
            non_category_count = 0
            total_processed = 0
            
            with open(csv_file_path, "r", encoding='utf-8') as csvfile:
                csv_reader = csv.reader(csvfile, delimiter=",")  # Use semicolon ; delimiter if needed
                headers = next(csv_reader)
                print(f"Function headers: {headers}")

                for row_index, row in enumerate(csv_reader, start=1):
                    if len(row) < len(headers):
                        continue  # Skip incomplete rows
                        
                    exampletwo_id = safe_get_value(row, headers, "ExampleTwoID") #foreign key to ExampleTwo
                    examplefour_id = safe_get_value(row, headers, "ExampleFourID") #primery key to ExampleFour
                    category_status = safe_get_value(row, headers, "YesOrNot") #indicates if it's category or not
                    #Create function URI
                    thing4_uri = create_uri("Thing4", examplefour_id, default_ns)
                    if is_bad_id(examplefour_id):
                        continue


                    # Apply filter if specified
                    if target_examplefour_id and normalize_id(examplefour_id) != normalize_id(target_examplefour_id):
                        continue         
                    if target_exampletwo_id and normalize_id(exampletwo_id) != normalize_id(target_exampletwo_id):
                        continue

                    total_processed += 1
                    # Check if it's a category function
                    if not is_blank(category_status):
                        is_category = category_status.strip().lower() in {'y', 'yes', 'j', 'ja', 'true', '1'}
                        if is_category:
                            # Add category functions to the graph
                            
                            
                            self.graph.add((thing4_uri, RDF.type, onto_ns.ItemCategory))
                            self.graph.add((thing4_uri, RDF.type, onto_ns.CategoryFunctie))
                            self.graph.add((thing4_uri, RDFS.label, Literal(examplefour_id, datatype=XSD.string)))

                            category_count += 1
                            print(f"Added category function: {examplefour_id}")
                        else:
                            # Add non-category functions to the graph
                            self.graph.add((thing4_uri, RDF.type, onto_ns.ItemCategory))
                            self.graph.add((thing4_uri, RDFS.label, Literal(examplefour_id, datatype=XSD.string)))

                            # Note: Non-category functions are not typed as 'Category'
                            non_category_count += 1
                            print(f"Added non-category function: {examplefour_id}")
                    else:
                        # Skip functions with blank category status (don't add to graph)
                        non_category_count += 1
                        print(f"Skipped function with blank category status: {examplefour_id}")

            print(f"Completed processing functions:")
            print(f"  Total processed: {total_processed}")
            print(f"  Category: {category_count}")
            print(f"  Non-Category: {non_category_count}")

            return total_processed

    def get_graph(self):
        """Get the function graph."""
        return self.graph

    def save_graph(self, filename, format='turtle'):
        """Save the function graph to file."""
        self.graph.serialize(destination=filename, format=format)
        print(f"Function RDF saved to {filename}")

    def get_triples_count(self):
        """Get number of triples in the graph."""
        return len(self.graph)