from rdflib import Graph
from .namespaces import NAMESPACES

class GraphManager:
    def __init__(self):
        self.graph = Graph()
        for prefix, ns in NAMESPACES.items():
            self.graph.bind(prefix, ns)

    def add_triple(self, subject, predicate, obj):
        """Add a triple to the graph."""
        self.graph.add((subject, predicate, obj))

    def serialize(self, format='turtle'):
        """Serialize the graph to a string."""
        return self.graph.serialize(format=format)
    
    def save_to_file(self, file_path, format='turtle'):
        """Save the graph to a file."""
        self.graph.serialize(destination=file_path, format=format)
    
    def size(self):
        """Return the number of triples in the graph."""
        return len(self.graph)
    def query(self, sparql_query):
        """Run a SPARQL query against the graph."""
        return self.graph.query(sparql_query)