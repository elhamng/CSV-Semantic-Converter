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

#create author class
class Author(Thing):
    """Class representing an author in the ontology."""
    namespace = onto

    pass
# create data properties for Author
class has_name(DataProperty):
    """Data property for the author's name."""
    namespace = onto
    domain = [Author]
    range = [str]

class has_birthdate(DataProperty):
    """Data property for the author's birthdate."""
    namespace = onto
    domain = [Author]
    range = [datetime.date]

class has_email(DataProperty):
    """Data property for the author's email."""
    namespace = onto
    domain = [Author]
    range = [str]

class has_affiliation(DataProperty):
    """Data property for the author's affiliation."""
    namespace = onto
    domain = [Author]
    range = [str]

class writes(ObjectProperty):
    """Object property linking an author to their written works."""
    namespace = onto
    domain = [Author]
    range = [Thing]  # Assuming 'Thing' represents a written work in the ontology    

class collaborates_with(ObjectProperty):
    """Object property linking an author to their collaborators."""
    namespace = onto
    domain = [Author]
    range = [Author]

