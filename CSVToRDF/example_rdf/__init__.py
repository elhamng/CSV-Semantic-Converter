"""
EXAMPLE RDF Conversion Package

A package for converting EXAMPLE CSV data to RDF/TTL format using ontology.
Version: 1.0.0
"""

# Import main converters for easy access
from .converters.exampleone_converter import ExampleOneConverter
from .converters.exampletwo_converter import ExampleTwoConverter
from .converters.examplethree_converter import ExampleThreeConverter
from .converters.examplefour_converter import ExampleFourConverter

from .pipeline import EXAMPLERDFProcessor
from .temporal_utils import DayInstanceGenerator, generate_dagen_standalone


# Import namespaces for convenient access
from .namespaces import (
    default_ns, 
    onto_ns, 
    time_ns,
    NAMESPACES
)

# Import utility functions
from .utils import (
    is_bad_id, 
    is_blank, 
    safe_get_value, 
    create_uri, 
    to_xsd_date, 
    normalize_id,
    to_decimal,
    extract_one_id
)

# Package metadata
__version__ = "1.0.0"
__author__ = "EXAMPLE RDF Team"
__description__ = "Convert EXAMPLE CSV data to RDF format with ontology"

# Define what gets imported when someone does "from example_rdf import *"
__all__ = [
    # Converters
    'ExampleOneConverter',
    'ExampleTwoConverter',
    'ExampleThreeConverter',
    'ExampleFourConverter',
    
    # Namespaces
    'default_ns',
    'onto_ns', 
    'time_ns',
    'NAMESPACES',
    
    # Data processing Utilities
    'is_bad_id',
    'is_blank', 
    'safe_get_value',
    'create_uri',
    'to_xsd_date',
    'normalize_id',
    'to_decimal',
    'extract_one_id',
    'create_time_instant',

    #Main Pipeline
    'EXAMPLERDFProcessor',

    # Temporal Utilities
    'DayInstanceGenerator',
    'generate_dagen_standalone',
    
    # Metadata
    '__version__',
]