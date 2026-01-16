import csv
from rdflib import RDF, RDFS, Literal, XSD
from ..namespaces import default_ns, onto_ns
from rdflib import BNode
from ..utils import is_bad_id, is_blank, safe_get_value, create_uri, to_xsd_date, normalize_id,to_decimal, create_time_instant

class ExampleTwoConverter:
    """ Converter class for processing exampletwo CSV data into RDF. """
    def __init__(self,graph):
        """Initialize with an RDF graph."""
        self.graph = graph

    def process_exampletwo_csv(self, csv_file_path,target_exampletwo_id=None,target_exampleone_id=None):
        """Process exampletwo CSV -> subjects and properties.
        Args:
            csv_file_path (str): Path to the exampletwo CSV file
            target_exampletwo_id (str, optional): Filter for specific exampletwo (e.g., "200010_1")
            target_exampleone_id (str, optional): Filter for specific exampleone (e.g., "200010")


        """
        print(f"Processing exampletwo from: {csv_file_path}")

        if target_exampletwo_id:
            print(f"  → Filtering for ExampleTwoID: {target_exampletwo_id}")

        if target_exampleone_id:
            print(f"  → Filtering for ExampleOneID: {target_exampleone_id}")

        with open(csv_file_path, "r", encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=",")
            headers = next(csv_reader)
            print(f"ExampleTwo headers: {headers}")

            processed_count = 0
            for row_index, row in enumerate(csv_reader, start=1):
                

                exampletwo_id = safe_get_value(row, headers, "ExampleTwoID") #primery key to ExampleTwo
                exampleone_id   = safe_get_value(row, headers, "ExampleOneID") #foreign key to ExampleTwo
                if is_bad_id(exampletwo_id):
                    continue

                # Apply filters if specified - ADD ACTUAL FILTERING LOGIC
                if target_exampletwo_id and normalize_id(exampletwo_id) != target_exampletwo_id:
                    continue

                if target_exampleone_id and normalize_id(exampleone_id) != target_exampleone_id:
                    continue


                if target_exampletwo_id:
                    print(f"  → Filtering for ExampleTwoID: {target_exampletwo_id}")

                if target_exampleone_id:
                    print(f"  → Filtering for ExampleOneID: {target_exampleone_id}")

                print(f"Processing exampletwo: ExampleTwoID={exampletwo_id}, ExampleOneID={exampleone_id}")

                example_type   = safe_get_value(row, headers, "SomeCategoryTypeID")
                example_group   = normalize_id(safe_get_value(row, headers, "SomeGroupID"))
                date_in_raw       = safe_get_value(row, headers, "DateIn", clean_spaces=False)
                date_out_raw      = safe_get_value(row, headers, "DateOut", clean_spaces=False)
                hours_raw     = safe_get_value(row, headers, "Hours", clean_spaces=False)
                
                
                # Create unique identifier for this change period
                unique_exampletwo_id = f"{exampletwo_id}_{row_index}"
                #Create URIs
                example_number = normalize_id(exampleone_id)
                thing1_uri = create_uri("Thing1", example_number, default_ns)
                thing2_uri = create_uri("Thing2", exampletwo_id, default_ns)

                self.graph.add((thing1_uri, RDF.type, onto_ns.Thingone))
                self.graph.add((thing1_uri, RDFS.label, Literal(example_number, datatype=XSD.string)))
                self.graph.add((thing2_uri, RDF.type, onto_ns.Thingtwo))
                self.graph.add((thing2_uri, RDFS.label, Literal(exampletwo_id, datatype=XSD.string)))

                # Dates with OWL-Time support for Indicator 1.1
                literal_start = to_xsd_date(date_in_raw)
                literal_end   = to_xsd_date(date_out_raw)
                if literal_start:
                    self.graph.add((thing1_uri, onto_ns.startDatum, literal_start))
                    # Create time instant for start date
                    create_time_instant(self.graph, literal_start)
                if literal_end:
                    self.graph.add((thing1_uri, onto_ns.eindDatum, literal_end))
                    # Create time instant for end date
                    create_time_instant(self.graph,literal_end)

                # some link thing1 and thing3 (ExampleGroup)
                if not is_blank(example_group):
                    group_uri = create_uri("Thing3", example_group, default_ns)

                    self.graph.add((group_uri, RDF.type, onto_ns.Thingthree))
                    self.graph.add((group_uri, RDFS.label, Literal(example_group, datatype=XSD.string)))
                    # Link to thing1
                    self.graph.add((thing1_uri, onto_ns.hassomeRelationship, group_uri))
                # Link to employee
                self.graph.add((thing1_uri, onto_ns.hasotherrelationship, thing2_uri))
                # Add example type as a category
                self._add_category_type(thing2_uri, example_type)
                # Example type as a quality (optional)
                if not is_blank(example_type):
                    qualitynode, valuenode = BNode(), BNode()
                    self.graph.add((thing1_uri, onto_ns.hasQuality, qualitynode))
                    self.graph.add((qualitynode, onto_ns.hasQualityValue, valuenode))
                    self.graph.add((valuenode, onto_ns.hasDataValue, Literal(example_type)))

                # ---- ContractOmvang (hours/week) ----
                if not is_blank(hours_raw):
                    self._process_hours(thing2_uri, unique_exampletwo_id, hours_raw, literal_start)

                processed_count += 1

        print(f"Completed processing {processed_count} contracts.")
        return processed_count

    def _add_category_type(self, thing3_uri, example_type):

        """Helper function to add example type based on value."""
        if not example_type or example_type.strip() == "":
            print(f"Warning: Empty example type for {thing3_uri}")
            # Don't return early - add a generic type instead
            self.graph.add((thing3_uri, RDF.type, onto_ns.GenericExampleType))

            return

        # Clean the example type (remove spaces, convert to lowercase for comparison)
        clean_example_type = example_type.strip()

        type_mapping = {
            # Permanent contracts
            'A': onto_ns.ExampleTypeA,
            'B': onto_ns.ExampleTypeB,
            'C': onto_ns.ExampleTypeC,
            'D': onto_ns.ExampleTypeD
        }

        # Try exact match first
        if clean_example_type in type_mapping:
            example_class = type_mapping[clean_example_type]
            self.graph.add((thing3_uri, RDF.type, example_class))
            print(f" Added example type: {clean_example_type} -> {example_class}")
            return
        
        # Try case-insensitive match
        clean_lower = clean_example_type.lower()
        for key, value in type_mapping.items():
            if key.lower() == clean_lower:
                self.graph.add((thing3_uri, RDF.type, value))
                print(f" Added example type (case-insensitive): {clean_example_type} -> {value}")
                return
        
        # If no match found, add as generic work agreement and log warning
        print(f"  Unknown example type: '{example_type}' - using generic GenericExampleType")
        self.graph.add((thing3_uri, RDF.type, onto_ns.GenericExampleType))


    def _process_hours(self, thing2_uri, unique_exampletwo_id, hours_raw, start_date_literal):
        """Helper function to process contract hours/week into RDF triples."""
        try:
            hours = to_decimal(hours_raw)
            if hours is None:
                print(f"  Invalid hours value: '{hours}' for {unique_exampletwo_id}")
                return

            # Create a blank node for the contract hours
            calculate_hours_node = BNode()
            self.graph.add((thing2_uri, onto_ns.hasHours, calculate_hours_node))
            self.graph.add((calculate_hours_node, RDF.type, onto_ns.Hours))
            self.graph.add((calculate_hours_node, onto_ns.hoursUnit, Literal(hours, datatype=XSD.decimal)))

            # Optionally link to time instant if start date is provided
            if start_date_literal:
                create_time_instant(self.graph, start_date_literal)

        except Exception as e:
            print(f"  Error processing contract hours for {unique_exampletwo_id}: {e}")
