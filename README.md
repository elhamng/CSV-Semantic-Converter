# CSV-Semantic-Converter
SPARQL is a query language for graph databases, specifically for RDF triple stores such as GraphDB.

The core idea of SPARQL is that we define a graph pattern in the WHERE clause. This pattern describes the structure of the data we want to match in the graph.

In the SELECT clause, we specify which parts of that matched pattern we want to return to the user.

When defining a pattern, we can use fixed values or variables. Fixed values are expressed as IRIs or literals, while variables are prefixed with a question mark (?).

In this example, all three elements of the triple — subject, predicate, and object — are variables. This means we are matching all triples in the dataset, without any restrictions.

Finally, by selecting all three variables, we return the complete set of triples that match this pattern.
