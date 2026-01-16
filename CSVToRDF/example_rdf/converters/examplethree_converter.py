import csv
from rdflib import RDF, RDFS, Literal, XSD,BNode
from ..namespaces import default_ns, onto_ns
from ..utils import is_bad_id, is_blank, safe_get_value, create_uri, to_xsd_date, normalize_id,to_decimal, create_time_instant

class ExampleThreeConverter:
    """ Converter class for processing ExampleThree CSV data into RDF. """
    def __init__(self,graph):
        """Initialize with an RDF graph."""
        self.graph = graph
    def process_example_three_csv(self,csv_file_path,target_exampletwo_id=None,target_exampleone_id=None):
        """Process ExampleThree CSV -> Thing3 + ExamplePeriode.
        Args:
            csv_file_path (str): Path to the ExampleThree CSV file
            target_exampletwo_id (str, optional): Filter for specific example (e.g., "1")
            target_exampleone_id (str, optional): Filter for specific example (e.g., "2")
        """
        print(f"Processing examples from: {csv_file_path}")

        if target_exampletwo_id:
            print(f"  → Filtering for ExampleTwoID: {target_exampletwo_id}")
        if target_exampleone_id:
            print(f"  → Filtering for ExampleOneID: {target_exampleone_id}")

        with open(csv_file_path, "r", encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=",")
            headers = next(csv_reader)
            print(f"Example headers: {headers}")
            processed_count = 0
            for row_index, row in enumerate(csv_reader, start=1):
                exampletwo_id = safe_get_value(row, headers, "ExampleTwoID") #primery key to ExampleTwo
                exampleone_id   = normalize_id(safe_get_value(row, headers, "ExampleOneID")) #foreign key to ExampleTwo

                if is_bad_id(exampletwo_id):
                    continue
                # Apply filters if specified
                if target_exampletwo_id and normalize_id(exampletwo_id) != target_exampletwo_id:
                    continue

                if target_exampleone_id and normalize_id(exampleone_id) != target_exampleone_id:
                    continue

                # Extract data fields
                #exampleone_id = safe_get_value(row, headers, 'ExampleOneID')
                #example_number_value = safe_get_value(row, headers, 'Number')
                examplethree_id_value = safe_get_value(row, headers, 'ExampleThreeID')
                start_date_raw = safe_get_value(row, headers, 'START_DATE_RAW',clean_spaces=False)
                end_date_raw = safe_get_value(row, headers, 'END_DATE_RAW',clean_spaces=False)
                hours_raw = safe_get_value(row, headers, 'HOURS_RAW', clean_spaces=False)

                print(f"Processing change row {row_index}: {exampletwo_id}, {exampleone_id}, {examplethree_id_value}")

                # Create unique identifier for this change period
                unique_exampletwo_id = f"{exampletwo_id}_{row_index}"

                thing1_uri = create_uri("Thing1", exampleone_id, default_ns)

                # Link to existing things (from main exampletwo processing)
                thing2_uri = create_uri("Thing2", exampletwo_id, default_ns)
                thing3_uri = create_uri("Thing3", examplethree_id_value, default_ns)
                thing4_uri = create_uri("thing4", unique_exampletwo_id, default_ns)


                self.graph.add((thing2_uri, RDF.type, onto_ns.Thingtwo))
                self.graph.add((thing2_uri, RDFS.label, Literal(exampletwo_id, datatype=XSD.string)))
                self.graph.add((thing2_uri, onto_ns.hasPart, thing4_uri))
                self.graph.add((thing4_uri, RDF.type, onto_ns.ThingFour))
                self.graph.add((thing4_uri, RDFS.label, Literal(unique_exampletwo_id, datatype=XSD.string)))
                #self.graph.add((werkovereenkomstAfspraak_uri, onz_g_ns.isAbout,onz_g_ns.OccupationalPositionRole))  # General type
                self.graph.add((thing4_uri, onto_ns.isAbout, thing3_uri))

                # Add time period for this agreement
                # Dates
                literal_start = to_xsd_date(start_date_raw)
                literal_end   = to_xsd_date(end_date_raw)
                

                if literal_start:
                    self.graph.add((thing4_uri, onto_ns.startDatum, literal_start))
                    create_time_instant(self.graph, literal_start)
                if literal_end:
                    self.graph.add((thing4_uri, onto_ns.eindDatum, literal_end))
                    create_time_instant(self.graph, literal_end)
                # Some role
                if not is_blank(examplethree_id_value):
                    function_uri = create_uri("ExampleThree", examplethree_id_value, default_ns)
                    self.graph.add((function_uri, RDF.type, onto_ns.SomeRole))
                    self.graph.add((function_uri, RDFS.label, Literal(examplethree_id_value, datatype=XSD.string)))
                    # DIRECT relationship - satisfies ontology constraint
                    self.graph.add((thing4_uri, onto_ns.isAbout, thing2_uri))

                print(f"   Added role: {examplethree_id_value}")
                # Process Hours if available
                hours_decimal = to_decimal(hours_raw)
                if hours_decimal:
                    self._process_period(thing3_uri, unique_exampletwo_id, thing1_uri, thing2_uri, hours_decimal, literal_start, literal_end)
                processed_count += 1
            
        print(f"Completed processing {processed_count} contracts.")
        return processed_count
    
    def _process_period(self, thing3_uri, unique_exampletwo_id, thing1_uri, thing2_uri, hours_decimal, literal_start, literal_end):
        """Process period and related entities."""
        period_uri = create_uri("Period", unique_exampletwo_id, default_ns)
        self.graph.add((period_uri, RDF.type, onto_ns.Period))
        self.graph.add((period_uri, onto_ns.definedBy, thing2_uri))
        self.graph.add((period_uri, onto_ns.hasParticipant, thing3_uri))
        self.graph.add((period_uri, onto_ns.hasArtifact, thing1_uri))
        if hours_decimal:
            self.graph.add((period_uri, onto_ns.hasHours, hours_decimal))
        if literal_start:
            self.graph.add((period_uri, onto_ns.startDatum, literal_start))
        if literal_end:
            self.graph.add((period_uri, onto_ns.eindDatum, literal_end))
        
        print(f"   Added period: {unique_exampletwo_id} with hours: {hours_decimal}")