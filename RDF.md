In RDF, anything that can be described is modeled as a resource. Resources are identified by IRIs, which refer to real-world objects, abstract concepts, or documents. A resource identified by an IRI is called a referent. Concrete values such as strings, numbers, and dates are represented as literals, not resources, and literals have datatypes or language tags. RDF represents information using triples, where a predicate denotes a relationship between a subject resource and an object, which can be either another resource or a literal value.

1️⃣ Resource

In RDF, anything that can be talked about is a resource.

A resource can represent:

Physical things (a person, a hospital)

Abstract concepts (a contract, an agreement)

Events (a sickness period)

Documents

Classes and properties themselves

Important correction:
Numbers and strings are not resources in RDF — they are literals.

2️⃣ IRI (Internationalized Resource Identifier)

An IRI is a global identifier used to identify a resource.

Examples:

http://example.org/person/123

A resource denoted by an IRI is called a referent

The IRI refers to the resource (real-world or conceptual)

👉 In RDF:

IRI = identifier

Resource = what the IRI refers to

3️⃣ Literal (literal value)

A literal represents a concrete value, not a thing.

Examples:

Strings

Numbers

Dates

Booleans

Literals:

Do not have IRIs

Cannot be subjects

Do not denote resources

Examples:

"Alice"@nl

"2023-01-01"^^xsd:date

"32"^^xsd:decimal


👉 Correct terminology:

A resource identified by an IRI is a resource

A value like a string or number is a literal value



