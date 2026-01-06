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

4️⃣ Datatypes for literals

Every literal has:

a lexical form (the written text)

optionally a datatype

optionally a language tag

Examples:

"32"^^xsd:integer
"2023-01-01"^^xsd:date
"Alice"@en


This is how RDF keeps values precise and machine-interpretable.

5️⃣ Entity vs Resource

Entity is a conceptual term (often used in modeling and KG discussions)

Resource is the formal RDF term

So in practice:

Entity ≈ Resource identified by an IRI

But strictly:

RDF uses resource

Knowledge graph literature often says entity

6️⃣ RDF Triples

An RDF triple has three parts:

subject — predicate — object


Formally:

Subject: IRI or blank node (resource)

Predicate: IRI (property)

Object: IRI / blank node (resource) or literal

Example (resource → resource):

:Contract_1 onto:hasemployee :Person_123 .


Example (resource → literal):

:Contract_1 onto:hasstartdate "2023-01-01"^^xsd:date .

7️⃣ Predicate (relationship)

A predicate:

Is always an IRI

Represents a relationship or attribute

Connects subject and object

Two kinds:

Object property → object is a resource

Data property → object is a literal

IRI collisions occur when the same identifier is used to denote different real-world entities or when a single entity is unintentionally represented by multiple IRIs. Because RDF assumes that identical IRIs refer to the same thing, such collisions lead to semantic corruption of the knowledge graph. Careful IRI design—incorporating explicit scoping, entity typing, and stable identifier strategies—is therefore essential to preserve identity, accuracy, and long-term maintainability.

Core principles of good IRI design

✅ 1. One real-world thing → one IRI

Never reuse an IRI for another thing.

✅ 2. Include entity type in the path

This avoids cross-type collisions.

/person/{id}
 /contract/{id}
 /organization/{id}



