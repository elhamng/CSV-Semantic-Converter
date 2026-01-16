import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, current_dir)
try:
    from .onto import onto  # Relative import
except ImportError:
    from onto import onto  # Absolute import
try:

    from .classes.author import Author, has_affiliation, has_birthdate, has_email, has_name, writes, collaborates_with
    from .classes.book import Book, has_ISBN, has_publication_date, has_title, has_author
    from .classes.publisher import Publisher, has_established_year, has_location, has_publisher_name, has_website, publishes_book
except ImportError:
    from classes.author import Author, has_affiliation, has_birthdate, has_email, has_name, writes, collaborates_with
    from classes.book import Book, has_ISBN, has_publication_date, has_title, has_author
    from classes.publisher import Publisher, has_established_year, has_location, has_publisher_name, has_website, publishes_book

# The main.py file can be used to initialize the ontology and its classes
# Additional functionality can be added here as needed
# For example, creating instances or saving the ontology to a file
# Example: Saving the ontology to a file
#ontology class registry
ONTOLOGY_CLASS_REGISTRY = {
    'Author': Author,
    'Book': Book,
    'Publisher': Publisher
}

# Data property registry
DATA_PROPERTY_REGISTRY = {
    # Author properties
    'has_affiliation': has_affiliation,
    'has_birthdate': has_birthdate,
    'has_email': has_email,
    'has_name': has_name,
    # Book properties
    'has_ISBN': has_ISBN,
    'has_publication_date': has_publication_date,
    'has_title': has_title,
    # Publisher properties
    'has_established_year': has_established_year,
    'has_location': has_location,
    'has_publisher_name': has_publisher_name,
    'has_website': has_website,
}

# Object property registry
OBJECT_PROPERTY_REGISTRY = {
    'writes': writes,
    'collaborates_with': collaborates_with,
    # Book properties
    'has_author': has_author,
    # Publisher properties
    'publishes_book': publishes_book
}

# Combine all registries into a single registry for easy access
ONTOLOGY_SCHEMA = {
    'classes': ONTOLOGY_CLASS_REGISTRY,
    'data_properties': DATA_PROPERTY_REGISTRY,
    'object_properties': OBJECT_PROPERTY_REGISTRY,
    'ontology': onto
}

def get_ontology_schema():
    """
    Returns the complete ontology schema including classes, data properties, and object properties."""
    return ONTOLOGY_SCHEMA

def save_ontology(file_path: str):
    """
    Saves the ontology to the specified file path in RDF/XML format.
    
    :param file_path: The path where the ontology should be saved.
    """
    onto.save(file=file_path, format="rdfxml")
    print(f"Ontology saved to {file_path}")


main_ontology_schema = get_ontology_schema()

if __name__ == "__main__":
    # Example usage: Save the ontology to a file
    save_ontology("book_publishing_ontology.owl")