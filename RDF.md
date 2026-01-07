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

 Unicode defines a universal set of characters for representing text from all writing systems, while UTF-8 is a byte-level encoding that represents Unicode characters efficiently and compatibly with ASCII. UTF-8 has become the standard encoding for web technologies, APIs, RDF, and knowledge graphs. Correct handling of Unicode and UTF-8 is essential to preserve labels, literals, multilingual content, and IRIs without data corruption.

 In RDF, a datatype is defined by its lexical space, which specifies the set of valid string representations, its value space, which defines the abstract values those strings represent, and a lexical-to-value mapping that interprets strings as values. Different lexical forms may map to the same value, and comparisons in SPARQL operate on value spaces rather than lexical forms. Ill-typed literals, whose lexical forms fall outside the datatype’s lexical space, can lead to inconsistent or undefined behavior and should be avoided.
 Lexical Space — “What strings are allowed?”

The lexical space is the set of strings that are valid representations for a datatype.

Example: xsd:integer

Lexical space includes:

"0" ,
"1",
"-42", \n
"+7", \n
"0005"


Lexical space excludes:

"1.5",
"one",
"1,000",


All of these are strings.

Example: xsd:date

Lexical space:

"2023-01-01",
"1999-12-31"


Invalid lexical forms:

"01-01-2023",
"2023/01/01"

Value Space — “What values do they mean?”

The value space is the set of abstract values the datatype represents.

Example: xsd:integer

Value space:

…, -2, -1, 0, 1, 2, …


So:

"5",

"05",

"+5"

all map to the same value: 5

Example: xsd:boolean

Lexical space:

"true", "false", "1", "0"


Value space:

true, false


Mappings:

"true" → true

"1" → true

"false" → false

"0" → false

Lexical-to-Value Mapping — “How strings become values”

This mapping:

takes a lexical form (string)

interprets it according to the datatype

yields a value in the value space

Example: integers

Lexical form	Datatype	Value

"05"	xsd:integer	5 ,
"+5"	xsd:integer	5 ,
"5"	xsd:integer	5 ,

These literals are value-equal.

Equality depends on the value space (important!)

In RDF/SPARQL:

"5"^^xsd:integer,
"05"^^xsd:integer


➡️ They are equal in value.

But:

"5"^^xsd:string, 
"05"^^xsd:string


➡️ They are not equal (strings differ).

Ill-typed literals (critical pitfall)

If a lexical form is not in the lexical space, the literal is ill-typed.

"2023/01/01"^^xsd:date


This has:

lexical form "2023/01/01"

datatype xsd:date

❌ no value (invalid)

Ill-typed literals:

exist syntactically

but break reasoning and comparisons

7️SPARQL examples
Numeric comparison (value space used)

SELECT ?x WHERE {

  FILTER("05"^^xsd:integer = "5"^^xsd:integer)
  
}


✔ True

String comparison (lexical space used)

FILTER("05"^^xsd:string = "5"^^xsd:string)


❌ False

Date comparison

FILTER("2023-01-01"^^xsd:date < "2023-12-31"^^xsd:date)


✔ True

Ill-typed literal filter

FILTER("2023/01/01"^^xsd:date < "2023-12-31"^^xsd:date)


❌ Error / false / engine-dependent

8️⃣ Language-tagged strings (special case)

"Alice"@en

"Alice"@nl


They do not have a datatype

They have no value space beyond the string

Equality requires same language tag

FILTER("Alice"@en = "Alice"@nl)   # false

Why this matters in Knowledge Graphs

Bad datatype handling causes:

wrong comparisons

broken filters

silent query errors

inconsistent analytics

Especially dangerous in:

dates

percentages

numeric calculations

time periods

 



