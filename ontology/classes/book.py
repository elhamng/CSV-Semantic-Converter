from owlready2 import Thing, DataProperty, ObjectProperty, Ontology
from rdflib import Graph
import datetime
import os
import sys
try:
    from ..onto import onto # Import the shared ontology
except ImportError:
    current_dir =os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.insert(0, parent_dir)
    sys.path.insert(0, current_dir)
    from onto import onto # Import the shared ontology
from classes.author import Author
from classes.publisher import Publisher

#create book class
class Book(Thing):
    """Class representing a book in the ontology."""
    namespace = onto

    pass
# create data properties for Book
class has_title(DataProperty):
    """Data property for the book's title."""
    namespace = onto
    domain = [Book]
    range = [str]

class has_publication_date(DataProperty):
    """Data property for the book's publication date."""
    namespace = onto
    domain = [Book]
    range = [datetime.date]
class has_ISBN(DataProperty):
    """Data property for the book's ISBN."""
    namespace = onto
    domain = [Book]
    range = [str]    
#Object properties    

class has_author(ObjectProperty):
    """Object property for the book's author."""
    namespace = onto
    domain = [Book]
    range = [Author]  
class has_publisher(ObjectProperty):
    """Object property for the book's publisher."""
    namespace = onto
    domain = [Book]
    range = [Publisher]  # Assuming 'Publisher' represents a publisher in the ontology
