import csv
from rdflib import RDF, RDFS, Literal, XSD
from ..namespaces import default_ns, onto_ns
from ..utils import is_bad_id, is_blank, safe_get_value, create_uri, to_xsd_date,normalize_id

class ExampleOneConverter:
    """ Converter class for processing example one CSV data into RDF. """
    def __init__(self,graph):
        """Initialize with an RDF graph."""
        self.graph = graph
    def process_exampleone_csv(self, csv_file_path,target_exampleone_id=None):
        """Process exampleone CSV file -> onto:thing1.

        Args:
            csv_file_path (str): Path to the exampleone CSV file.
            target_graph (rdflib.Graph): RDF graph to add triples to.
        """
        print(f"Processing exampleone from: {csv_file_path}")
        if target_exampleone_id:
            print(f"  → Filtering for ExampleOneID: {target_exampleone_id}")

        with open(csv_file_path, "r", encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=",")
            headers = next(csv_reader)
            print(f"ExampleOne headers: {headers}")
            processed_count = 0
            for row_index, row in enumerate(csv_reader, start=1):
                #if row_index == 7:
                    #   break
                exampleone_id = safe_get_value(row, headers, "ExampleOneID")
                if is_bad_id(exampleone_id):
                    continue
                exampleone_id = normalize_id(exampleone_id)
                #process the example data

                #apply filter if specified
                if target_exampleone_id and exampleone_id != target_exampleone_id:
                    continue

                date_raw = safe_get_value(row, headers, "Date",clean_spaces=False)
                exampleone_uri = create_uri("Thing1", exampleone_id, default_ns)

                self.graph.add((exampleone_uri, RDF.type, onto_ns.Thingone))
                self.graph.add((exampleone_uri, RDFS.label, Literal(exampleone_id, datatype=XSD.string)))
                date = to_xsd_date(date_raw)
                if date:

                    self.graph.add((exampleone_uri, onto_ns.hasDate, date))
                processed_count += 1

                # Additional example properties can be added here
        print(f"Completed processing {processed_count} examples.")
        return processed_count