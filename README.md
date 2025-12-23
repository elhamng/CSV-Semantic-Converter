# CSV-Semantic-Converter

## SPARQL
SPARQL is a query language for graph databases, specifically for RDF triple stores such as GraphDB.

The core idea of SPARQL is that we define a graph pattern in the WHERE clause. This pattern describes the structure of the data we want to match in the graph.

In the SELECT clause, we specify which parts of that matched pattern we want to return to the user.

When defining a pattern, we can use fixed values or variables. Fixed values are expressed as IRIs or literals, while variables are prefixed with a question mark (?).

In this example, all three elements of the triple — subject, predicate, and object — are variables. This means we are matching all triples in the dataset, without any restrictions.

Finally, by selecting all three variables, we return the complete set of triples that match this pattern.

SELECT ?s ?p ?o

WHERE {?s ?p ?o}

## Finding classes in SPARQL

To find classes in an RDF dataset, we introduce two main concepts.

First, we can use an IRI to constrain the triples we want to match. In a triple pattern, the middle element is the predicate. If the predicate does not have a question mark in front of it, we know it is a fixed IRI rather than a variable.

In this case, we use the predicate rdf:type as a fixed IRI. This means we are not interested in returning the predicate itself; instead, we want to match all triples that assign something to a class — in other words, all triples of the form “resource is of type class.”

The second concept is the use of DISTINCT. Without DISTINCT, if multiple resources are instances of the same class, that class will appear multiple times in the result set. By using DISTINCT, we ensure that each class is returned only once, even if it is used by many different resources.

SELECT DISTINCT ?type

WHERE{?s a ?type}

In Turtle syntax, a subject can be shared across multiple predicate–object pairs.

When we do this, all predicate–object pairs for the same subject are written on separate lines. Each line except the last must end with a semicolon (;), and the final line must end with a (.).

This syntax makes RDF more compact and readable by avoiding repetition of the subject.

## Aggregation in SPARQL

Aggregation in SPARQL allows us to compute summary values over query results.

The COUNT function counts the number of bindings for a variable and binds the resulting value to a new variable.

Aggregation functions are typically used together with the GROUP BY clause, which defines how the results are grouped before the aggregation is applied.

In other words, GROUP BY specifies how individual matches are collected into groups, and aggregation functions such as COUNT produce a single value for each group.

example : a tiny sample dataset (Turtle)

@prefix ex:  <http://example.com/hr/> .

@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:Employee a rdf:Class .

ex:Contract a rdf:Class .

ex:hasContract a rdf:Property .

ex:e1 a ex:Employee .

ex:e2 a ex:Employee .

ex:e3 a ex:Employee .

ex:c1 a ex:Contract .

ex:c2 a ex:Contract .

ex:c3 a ex:Contract .

ex:c4 a ex:Contract .

ex:e1 ex:hasContract ex:c1 , ex:c2 .

ex:e2 ex:hasContract ex:c3 .

ex:e3 ex:hasContract ex:c4 .

Query: count contracts per employee

PREFIX ex:  <http://example.com/hr/>

PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?employee (COUNT(?contract) AS ?contractCount)

WHERE {
  ?employee rdf:type ex:Employee ;
  
            ex:hasContract ?contract .
}
GROUP BY ?employee

ORDER BY DESC(?contractCount)

What you’ll see (typical result)

ex:e1 → 2

ex:e2 → 1

ex:e3 → 1



