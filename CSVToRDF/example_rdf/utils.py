import pandas as pd
from rdflib import Graph, URIRef, Literal, XSD, RDF, RDFS, BNode
from rdflib.namespace import Namespace
from datetime import datetime   
from .namespaces import time_ns

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
    

def normalize_id(value):
    """Normalize ID by removing leading zeros and decimal points."""
    if pd.isna(value):
        return None
    value_str = str(value).strip()
    # Remove decimal part if exists
    if '.' in value_str:
        value_str = value_str.split('.')[0]
    # Remove leading zeros
    normalized = value_str.lstrip('0')
    return normalized if normalized else "0"

def is_blank(x):
    return x is None or str(x).strip() == ""

def is_bad_id(x):
    s = (x or "").strip()
    return s == "" or s == "-1"

def to_decimal(value):
    if is_blank(value): return None
    try:
        return Literal(float(str(value).replace(",", ".")), datatype=XSD.decimal)
    except Exception:
        return None    


def extract_one_id(main_id):
    """Extract employee number from ContractBK (first part before space or underscore)."""
    if is_blank(main_id):
        return None
    
    # Handle both spaces and underscores as separators
    main_str = str(main_id).strip()

    # Split on space first, then underscore
    if ' ' in main_str:
        return main_str.split(' ')[0]
    elif '_' in main_str:
        return main_str.split('_')[0]
    else:
        # If no separator, return the whole string
        return main_str

def to_xsd_date(date_str):
    """Return Literal(YYYY-MM-DD, xsd:date) or None."""
    #print(f" DEBUG to_xsd_date: input = '{s}' (type: {type(s)})")
    
    if is_blank(date_str): 
        #print("  → Blank input, returning None")
        return None
        
    txt = str(date_str).strip()
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
SENTINEL_DATES = {"0000-00-00", "0001-01-01", "1900-01-01", "1970-01-01","2999-12-31"}

def create_uri(entity_type, identifier, namespace=None):

    """
    Generates a URIRef for RDF triples.
    - entity_type (str): The type of entity (e.g., 'Thing1', 'Thing2').

    - identifier (str): A unique identifier for the entity (e.g., employee ID).
    - namespace (Namespace, optional): The RDF namespace to use. Defaults to default_ns.
    Returns:
        URIRef: The generated URIRef for the entity.
    """
    return URIRef(f"{namespace}{entity_type}_{identifier}")

# Cache to avoid creating duplicates
TIME_CACHE = {}
def create_time_instant(g, date_literal, base_epoch_date="2000-01-01"):
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
    
    # If we already created this date, return cached URIs
    if date_str in TIME_CACHE:
        return TIME_CACHE[date_str]
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
        #time_instant_uri = create_uri("TimeInstant", date_str.replace('-', '_'), default_ns)
        #temporal_position_uri = create_uri("TemporalPosition", date_str.replace('-', '_'), default_ns)
        # Create URI- using the format from the kik-v example
        time_instant_uri = URIRef(f"http://purl.org/ozo/onz-g/dag{date_str}")
        temporal_position = BNode()
        # Add RDF triples
        g.add((time_instant_uri, RDF.type, time_ns.Instant))
        g.add((time_instant_uri, time_ns.inXSDDate, Literal(date_str, datatype=XSD.date)))
        g.add((time_instant_uri, time_ns.inTemporalPosition, temporal_position))
        
        g.add((temporal_position, RDF.type, time_ns.TimePosition))
        g.add((temporal_position, time_ns.numericPosition, Literal(days_diff, datatype=XSD.integer)))
       
        # Save in cache
        TIME_CACHE[date_str] = (time_instant_uri, days_diff)
        
        return time_instant_uri, days_diff
        
    except Exception as e:
        print(f"Warning: Could not create time instant for date '{date_str}': {e}")
        return None, None
