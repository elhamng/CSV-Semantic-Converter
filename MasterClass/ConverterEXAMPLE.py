"""
CSV to RDF Converter for EXAMPLE Data Project

This module converts CSV data from EXAMPLE exports into RDF format using the ontology.
It processes various CSV files including example data information to generate semantic RDF triples.

Author: Elham Nour Ghassemi
Created: ....
Version: 1.0.0
Contact: ...
Organization: ...

Dependencies:
    - rdflib: For RDF graph manipulation
    - pandas: For CSV data processing
    - datetime: For date handling

Usage:
    python convert.py

The script will process CSV files from the data directory and generate 
RDF output in Turtle format.
"""
from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, XSD, BNode
import csv
import pandas as pd 
from datetime import datetime
import os


# Define common namespace URIs
#version = 3.0.0

default_s = 'http://data.default.nl#'
default_ns = Namespace(default_s)
onto_s = 'http://purl.org/onto#'
onto_ns = Namespace(onto_s)
# Add General ontology namespace
# Add Time namespace for temporal data
time_s = 'http://www.w3.org/2006/time#'
time_ns = Namespace(time_s)


g = Graph()

# Bind the namespace as the default namespace
g.bind("", default_ns)
g.bind('onto', onto_ns)
g.bind('time', time_ns)

def safe_get_value(row, headers, column_name, default="", clean_spaces=True):
    """Safely get value from CSV row with optional space cleaning."""
    try:
        if column_name in headers:
            value = row[headers.index(column_name)].strip()
            if clean_spaces:
                # Replace spaces with underscores for non-date fields
                return value.replace(' ', '_').replace('  ', '_')
            else:
                # Return as-is for date fields
                return value
        return default
    except (IndexError, ValueError):
        return default
def create_uri(entity_type, identifier, namespace=None):
    """
    Generates a URIRef for RDF triples.
    - entity_type (str): The type of entity (e.g., 'thing1', 'thing2').

    - identifier (str): A unique identifier for the entity (e.g., thing ID).
    - namespace (Namespace, optional): The RDF namespace to use. Defaults to default_ns.
    Returns:
        URIRef: The generated URIRef for the entity.
    """
    if namespace is None:
        namespace = default_ns
    return URIRef(f"{namespace}{entity_type}_{identifier}")
def normalize_id(IDid):
    """Normalize ID by removing leading zeros and decimal points."""
    if pd.isna(IDid):
        return ""
    IDid_str = str(IDid).strip()
    # Remove decimal part if exists
    if '.' in IDid_str:
        IDid_str = IDid_str.split('.')[0]
    # Remove leading zeros
    normalized = IDid_str.lstrip('0')
    return normalized if normalized else "0"

SENTINEL_DATES = {"01/01/1900", "01/01/1900 00:00:00", "12/31/2999", "12/31/2999 00:00:00"}

def is_blank(x):
    return x is None or str(x).strip() == ""

def is_bad_id(x):
    s = (x or "").strip()
    return s == "" or s == "-1"

def to_xsd_date(s):
    """Return Literal(YYYY-MM-DD, xsd:date) or None."""
    #print(f" DEBUG to_xsd_date: input = '{s}' (type: {type(s)})")
    
    if is_blank(s): 
        #print("  → Blank input, returning None")
        return None
        
    txt = str(s).strip()
    #print(f"  → After strip: '{txt}'")
    
    if txt in SENTINEL_DATES: 
        #print(f"  → Found sentinel date: '{txt}', returning None")
        return None
        
    if " " in txt:
        txt = txt.split(" ")[0]
        #print(f"  → After removing time: '{txt}'")
    
    # supports MM/DD/YYYY or DD-MM-YYYY
    if "/" in txt:
        #print(f"  → Processing slash format: '{txt}'")
        try:
            parts = txt.split("/")
            #print(f"  → Split parts: {parts}")
            m, d, y = parts
            result = Literal(f"{int(y):04d}-{int(m):02d}-{int(d):02d}", datatype=XSD.date)
            #print(f"  → SUCCESS: {result}")
            return result
        except Exception as e:
            #print(f"  → ERROR in slash processing: {e}")
            return None
            
    if "-" in txt:
        #print(f"  → Processing dash format: '{txt}'")
        try:
            parts = txt.split("-")
            #print(f"  → Split parts: {parts}")
            d, m, y = parts
            result = Literal(f"{int(y):04d}-{int(m):02d}-{int(d):02d}", datatype=XSD.date)
            #print(f"  → SUCCESS: {result}")
            return result
        except Exception as e:
            #print(f"  → ERROR in dash processing: {e}")
            return None
    
    print(f"  → No format matched, returning None")
    return None

def to_decimal(s):
    if is_blank(s): return None
    try:
        return Literal(float(str(s).replace(",", ".")), datatype=XSD.decimal)
    except Exception:
        return None

def create_time_instant(date_literal, base_epoch_date="2000-01-01"):
    """
    Create OWL-Time instant with numeric position for Indicator 1.1 queries.
    
    Args:
        date_literal: XSD date literal or date string
        base_epoch_date: Reference date for calculating numeric positions
    
    Returns:
        tuple: (time_instant_uri, numeric_position)
    """
    if date_literal is None:
        return None, None
    
    # Extract date string from literal or use directly
    if hasattr(date_literal, 'value'):
        date_str = str(date_literal.value)
    else:
        date_str = str(date_literal)
    
    # Parse the date
    try:
        if 'T' in date_str:
            date_str = date_str.split('T')[0]  # Remove time component
        
        # Parse YYYY-MM-DD format
        from datetime import datetime
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        base_date = datetime.strptime(base_epoch_date, '%Y-%m-%d').date()
        
        # Calculate days since epoch (numeric position)
        days_diff = (target_date - base_date).days
        
        # Create URIs
        time_instant_uri = create_uri("TimeInstant", date_str.replace('-', '_'), default_ns)
        temporal_position_uri = create_uri("TemporalPosition", date_str.replace('-', '_'), default_ns)
        
        # Add RDF triples
        g.add((time_instant_uri, RDF.type, time_ns.Instant))
        g.add((time_instant_uri, time_ns.inXSDDate, Literal(date_str, datatype=XSD.date)))
        g.add((time_instant_uri, time_ns.inTemporalPosition, temporal_position_uri))
        
        g.add((temporal_position_uri, RDF.type, time_ns.TimePosition))
        g.add((temporal_position_uri, time_ns.numericPosition, Literal(days_diff, datatype=XSD.integer)))
        
        return time_instant_uri, days_diff
        
    except Exception as e:
        print(f"Warning: Could not create time instant for date '{date_str}': {e}")
        return None, None

def extract_id_number(example_id):
    """Extract id number from thingid thingsid = number_id (first part before space or underscore)."""
    if is_blank(example_id):
        return None
    
    # Handle both spaces and underscores as separators
    example_str = str(example_id).strip()

    # Split on space first, then underscore
    if ' ' in example_str:
        return example_str.split(' ')[0]
    elif '_' in example_str:
        return example_str.split('_')[0]
    else:
        # If no separator, return the whole string
        return example_str

def add_from_dictionary(example_uri, example_type):
    """Helper function to add elements type based on value."""

    # Check if example_type is valid
    if not example_type or example_type.strip() == "":
        print(f"Warning: Empty example type for {example_uri}")
        # Don't return early - add a generic type instead
        g.add((example_uri, RDF.type, onto_ns.MYGenericExampleType))

        return

    # Clean the example type (remove spaces, convert to lowercase for comparison)
    clean_example_type = example_type.strip()

    type_mapping = {
        # Permanent examples
        'A': onto_ns.EXAMPLETYPEA,
        'B': onto_ns.EXAMPLETYPEB,
        'C': onto_ns.EXAMPLETYPEC,
        'D': onto_ns.EXAMPLETYPED
        }
    
    # Try exact match first
    if clean_example_type in type_mapping:
        example_class = type_mapping[clean_example_type]
        g.add((example_uri, RDF.type, example_class))
        print(f" Added example type: {clean_example_type} -> {example_class}")
        return
    
    # Try case-insensitive match
    clean_lower = clean_example_type.lower()
    for key, value in type_mapping.items():
        if key.lower() == clean_lower:
            g.add((example_uri, RDF.type, value))
            print(f" Added example type (case-insensitive): {clean_example_type} -> {value}")
            return
    
    # If no match found, add as generic work agreement and log warning
    print(f"  Unknown example type: '{example_type}' - using generic MYGenericExampleType ")
    g.add((example_uri, RDF.type, onto_ns.MYGenericExampleType))

def classify_some_category(example_category):
    """
    Classify example category values and return classification info.

    Args:
        example_category (str): The example category to classify

    Returns:
        dict: Classification results with 'is_healthcare'.
    """
    if is_blank(example_category):
        return {
            'is_categoryname': False,
            'category': 'unknown'
        }

    example_code = str(example_category).upper().strip()

    # Category codes - expanded for specific classifications
    Some_codes = {'code1', 'code2', 'code3'}
    
    # Check classifications
    is_category = any(code in example_code for code in Some_codes)
    # Determine primary category
    if is_category:
        category = 'some_category'
    else:
        category = 'other'
    
    return {
        'is_categoryname': is_category,
        'category': category,
        'original_code': example_category
    }
def process_exampleone_csv(csv_file_path):
    """Process exampleone CSV file -> onto:Exampleone."""
    print(f"Processing exampleone from: {csv_file_path}")
    with open(csv_file_path, "r", encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=",")
        headers = next(csv_reader)
        print(f"Exampleone headers: {headers}")

        for row_index, row in enumerate(csv_reader, start=1):
            #if row_index == 7:
             #   break
            exampleone_id = safe_get_value(row, headers, "HEAD_ID")
            if is_bad_id(exampleone_id):
                continue

            date_raw = safe_get_value(row, headers, "DATE_RAW",clean_spaces=False)
            exampleone_uri = create_uri("EXAMPLE", exampleone_id, default_ns)

            g.add((exampleone_uri, RDF.type, onto_ns.Exampleone))
            g.add((exampleone_uri, RDFS.label, Literal(exampleone_id, datatype=XSD.string)))
            date_raw = to_xsd_date(date_raw)
            if date_raw:
                # often uses schema:Date or an exampleone property; using generic label fallback:
                g.add((exampleone_uri, onto_ns.hasDate, date_raw))
            # Additional properties can be added here
    print(f"Completed processing exampleone.")


def process_exampletwo_csv(csv_file_path):
    """Process exampletwo CSV -> other subjects and properties."""
    print(f"Processing exampletwo from: {csv_file_path}")

    with open(csv_file_path, "r", encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=",")
        headers = next(csv_reader)
        print(f"Exampletwo headers: {headers}")

        for row_index, row in enumerate(csv_reader, start=1):
            #if row_index == 7:
             #   break

            exampletwo_id = safe_get_value(row, headers, "ExampleTwoID")
            if is_bad_id(exampletwo_id):
                continue

            # Extract relevant fields
            head_id = safe_get_value(row, headers, "HEAD_ID")
            date_raw = safe_get_value(row, headers, "DATE_RAW", clean_spaces=False)

            exampletwo_number = normalize_id(exampletwo_id)
            exampletwo_uri = create_uri("EXAMPLETWO", exampletwo_number, default_ns)
            exampletwo_uri = create_uri("EXAMPLETWO", f"{head_id}_{row_index}", default_ns)
            g.add((exampletwo_uri, RDF.type, onto_ns.Exampletwo))
            g.add((exampletwo_uri, RDFS.label, Literal(exampletwo_number, datatype=XSD.string)))
            date_raw = to_xsd_date(date_raw)
            if date_raw:
                g.add((exampletwo_uri, onto_ns.hasDate, date_raw))
            # Additional properties can be added here
    print(f"Completed processing exampletwo.")
def process_examplethree_csv(csv_file_path):
    """Process examplethree CSV -> onto:Examplethree and related entities."""


    with open(csv_file_path, "r", encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=",")
        headers = next(csv_reader)
        print(f"Examplethree headers: {headers}")

        for row_index, row in enumerate(csv_reader, start=1):
            #if row_index == 7:
            #   break

            examplethree_id = safe_get_value(row, headers, "ExampleThreeID")
            if is_bad_id(examplethree_id):
                continue

            # Extract relevant fields
            head_id = safe_get_value(row, headers, "HEAD_ID")
            start_date_raw = safe_get_value(row, headers, "START_DATE_RAW", clean_spaces=False)
            end_date_raw = safe_get_value(row, headers, "END_DATE_RAW", clean_spaces=False)
            date_in_raw = safe_get_value(row, headers, "DATE_IN_RAW", clean_spaces=False)

            #medewerker_number = extract_medewerker_number(contract_bk)
            examplethree_number = normalize_id(examplethree_id)
            examplethree_uri = create_uri("EXAMPLETHREE", examplethree_number, default_ns)
            examplethree_uri = create_uri("EXAMPLETHREE", f"{head_id}_{row_index}", default_ns)
            g.add((examplethree_uri, RDF.type, onto_ns.Examplethree))
            g.add((examplethree_uri, RDFS.label, Literal(examplethree_number, datatype=XSD.string)))
            start_date_raw = to_xsd_date(start_date_raw)
            if start_date_raw:
                g.add((examplethree_uri, onto_ns.hasStartDate, start_date_raw))
            # Additional properties can be added here
            # Dates with OWL-Time semantics
            literal_start = to_xsd_date(date_in_raw)
            literal_end   = to_xsd_date(end_date_raw)
            if literal_start:
                g.add((examplethree_uri, onto_ns.hasStartDate, literal_start))
                # Create time instant for start date
                create_time_instant(literal_start)
            if literal_end:
                g.add((examplethree_uri, onto_ns.hasEndDate, literal_end))
                # Create time instant for end date
                create_time_instant(literal_end)
    print(f"Completed processing examplethree.")




def save_rdf(output_path, format_type='turtle'):
    """Save the RDF graph to file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    g.serialize(destination=output_path, format=format_type)
    print(f"RDF data saved to: {output_path}")

def main():
    """Main function to process CSV files."""
    csv_directory = "inputdata/"
    
    # Check if directory exists
    if not os.path.exists(csv_directory):
        print(f" Directory not found: {csv_directory}")
        return
    
    # List all CSV files in directory
    csv_files = [f for f in os.listdir(csv_directory) if f.endswith('.csv')]
    print(f"Found CSV files: {csv_files}")
    
    # Process exampleone CSV
    exampleone_csv = os.path.join(csv_directory, "exampleone.csv")
    if os.path.exists(exampleone_csv):
        process_exampleone_csv(exampleone_csv)
        print(" Example One CSV processed")
    else:
        print(" exampleone.csv not found")

    # Process exampletwo CSV
    exampletwo_csv = os.path.join(csv_directory, "exampletwo.csv")
    if os.path.exists(exampletwo_csv):
        process_exampletwo_csv(exampletwo_csv)
        print(" Example Two CSV processed")
    else:
        print(" exampletwo.csv not found")

    # Process examplethree CSV
    examplethree_csv = os.path.join(csv_directory, "examplethree.csv")
    if os.path.exists(examplethree_csv):
        process_examplethree_csv(examplethree_csv)
        print(" Example Three CSV processed")
    else:
        print(" examplethree.csv not found")

    # Save RDF output
    output_file = "c:/RDFMapping/Output/example_rdf_Core.ttl"
    save_rdf(output_file, 'turtle')

    # Print statistics
    print(f"\n RDF Generation Statistics:")
    print(f"   Total triples: {len(g)}")
    print(f"   Unique subjects: {len(set(g.subjects()))}")

if __name__ == "__main__":
    main()