from owlready2 import get_ontology  

# Create a single shared ontology
onto = get_ontology("http://example.org/book_publishing_ontology#")

# Export it so other modules can use it
__all__ = ['onto']