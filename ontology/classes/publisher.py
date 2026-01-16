from owlready2 import Thing, DataProperty, ObjectProperty
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

#create publisher class
class Publisher(Thing):
    """Class representing a publisher in the ontology."""
    namespace = onto

    pass    

# create data properties for Publisher
class has_publisher_name(DataProperty):
    """Data property for the publisher's name."""
    namespace = onto
    domain = [Publisher]
    range = [str]

class has_established_year(DataProperty):
    """Data property for the publisher's established year."""
    namespace = onto
    domain = [Publisher]
    range = [int]

class has_location(DataProperty):
    """Data property for the publisher's location."""
    namespace = onto
    domain = [Publisher]
    range = [str]
class has_website(DataProperty):
    """Data property for the publisher's website."""
    namespace = onto
    domain = [Publisher]
    range = [str]

class publishes(ObjectProperty):
    """Object property linking a publisher to their published works."""
    namespace = onto
    domain = [Publisher]
    range = [str]  

#Object properties
class publishes_book(ObjectProperty):
    """Object property linking a publisher to the books they publish."""
    namespace = onto
    domain = [Publisher]
    range = [Thing]  # Assuming 'Thing' represents a book in the ontology