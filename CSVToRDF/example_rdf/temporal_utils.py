from datetime import date, timedelta, datetime
from rdflib.namespace import RDF, OWL, SKOS, RDFS, XSD, NamespaceManager
from rdflib import URIRef, BNode, Literal, Graph, Namespace
import os

class DayInstanceGenerator:
    """ Generate OWL-Time day instances with numerical positions. """
    def __init__(self, graph=None ):

        if graph is None:
            self.graph = Graph()
        else:
            self.graph = graph
        # set up namespaces
        self.DATA = Namespace("http://purl.org/ozo/onz-data/")
        self.TIME = Namespace('http://www.w3.org/2006/time#')
        
        self.graph.namespace_manager = NamespaceManager(Graph())
        #Bind namespaces
        self.graph.namespace_manager.bind('data', self.DATA)
        self.graph.namespace_manager.bind('time', self.TIME)

    def generate_day_instances(self, start_year, end_year):
        """Create instances for each day in the given period with a numerical position."""
        start_date=date(start_year, 1, 1)
        end_date=date(end_year, 12, 31)      
        reference_date = date(1900, 1, 1)
        generated_count = 0
        total_days = (end_date - start_date).days + 1
        
        print(f"Generating day instances from {start_date} to {end_date} ({total_days} days)")
        for i in range(total_days):
            datum = start_date + timedelta(days=i)
            volgnummer = (datum - reference_date).days + 1
            # Create URI- using the format from the kik-v example
            datumURI = URIRef('http://purl.org/ozo/onz-g/dag' + str(datum))
            TemporalPosition = BNode()
            # Add triples to the graph-exactly as in the original code
            self.graph.add((datumURI, RDF.type, self.TIME.Instant))
            self.graph.add((datumURI, self.TIME.inXSDDate, Literal(str(datum), datatype=XSD.date)))
            self.graph.add((datumURI, self.TIME.inTemporalPosition, TemporalPosition))
            self.graph.add((TemporalPosition, RDF.type, self.TIME.TimePosition))
            self.graph.add((TemporalPosition, self.TIME.numericPosition, Literal(volgnummer)))
            generated_count += 1

            if generated_count % 365 == 0:
                print(f"  Generated {generated_count}/{total_days} day instances so far...")
        print(f"Generated {generated_count} day instances.")
        return generated_count

    def generate_period(self, year=2011, include_buffer=True):
        """Generate day instances for data period.
        
        Args:
            year (int): Main year for data
            include_buffer (bool): Include surrounding months for contracts
            
        Returns:
            int: Number of day instances generated
        """
        if include_buffer:
            # Include some buffer for contracts that might extend beyond year
            start_datum = date(year - 1, 7, 1)  # Start mid-previous year
            eind_datum = date(year + 1, 6, 30)   # End mid-next year
            print(f"Period with buffer: {start_datum} to {eind_datum}")
        else:
            start_datum = date(year, 1, 1)
            eind_datum = date(year, 12, 31)
            print(f"Period exact year: {start_datum} to {eind_datum}")

        return self.generate_day_instances(start_datum, eind_datum)

    def serialize_graph(self, filename='days.ttl', format='turtle'):
        """Serialize the graph to a file."""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        self.graph.serialize(destination=filename, format=format)
        print(f"Day instances serialized to: {filename}")


    def get_triples_count(self):
        """Get number of triples in the graph."""
        return len(self.graph)

    def get_day_uri(self, datum):
        """Get URI for a specific day.
        
        Args:
            datum (date): The date
            
        Returns:
            URIRef: Day instance URI
        """
        return URIRef(f'http://purl.org/ozo/onz-g/dag{str(datum)}')

def generate_dagen_standalone(start_year=2020, end_year=2025, output_file='days.ttl'):
    """Standalone function matching your original script exactly."""
    print(f"Generating standalone day instances {start_year}-{end_year}")
    
    # Create generator and run
    generator = DayInstanceGenerator()
    count = generator.generate_day_instances(start_year, end_year)
    
    # Save exactly like your original
    generator.serialize_graph(output_file)
    
    return count

def main():
    """Example usage - matches your original script."""
    print("Day Instance Generator")
    print("=" * 50)
    
    # Option 1: Use your original date range (2020-2025)
    count = generate_dagen_standalone(2020, 2025, 'days.ttl')
    
    # Option 2: Generate for specific period
    # generator = DayInstanceGenerator()
    # count = generator.generate_period(2011)
    # generator.serialize_graph('example_days.ttl')

    print(f"\nGenerated {count} day instances")

if __name__ == "__main__":
    main()    