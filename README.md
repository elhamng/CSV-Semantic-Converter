# CSV-Semantic-Converter

##SPARQL
SPARQL is a query language for graph databases, specifically for RDF triple stores such as GraphDB.

The core idea of SPARQL is that we define a graph pattern in the WHERE clause. This pattern describes the structure of the data we want to match in the graph.

In the SELECT clause, we specify which parts of that matched pattern we want to return to the user.

When defining a pattern, we can use fixed values or variables. Fixed values are expressed as IRIs or literals, while variables are prefixed with a question mark (?).

In this example, all three elements of the triple — subject, predicate, and object — are variables. This means we are matching all triples in the dataset, without any restrictions.

Finally, by selecting all three variables, we return the complete set of triples that match this pattern.

SELECT ?s ?p ?o
WHERE {?s ?p ?o}

##Finding classes in SPARQL

To find classes in an RDF dataset, we introduce two main concepts.

First, we can use an IRI to constrain the triples we want to match. In a triple pattern, the middle element is the predicate. If the predicate does not have a question mark in front of it, we know it is a fixed IRI rather than a variable.

In this case, we use the predicate rdf:type as a fixed IRI. This means we are not interested in returning the predicate itself; instead, we want to match all triples that assign something to a class — in other words, all triples of the form “resource is of type class.”

The second concept is the use of DISTINCT. Without DISTINCT, if multiple resources are instances of the same class, that class will appear multiple times in the result set. By using DISTINCT, we ensure that each class is returned only once, even if it is used by many different resources.

SELECT DISTINCT ?type
WHERE{?s a ?type}
