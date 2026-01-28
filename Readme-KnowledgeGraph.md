A Knowledge Graph is a data artifact that represents entities (things in real world) and the relationships between them using explicit, shared semantics.

While the underlying ideas are rooted in earlier concepts such as semantic networks, ontologies, and linked data, modern knowledge graphs emphasize self-describing semantics, standardized technologies (RDF, OWL, SPARQL), and practical use at scale.

Knowledge graphs can be scoped to a single domain or span multiple domains and are commonly used for data integration, advanced analytics, and AI-driven applications.

A knowledge graph is an artifact that consists of entities that are connected to each other under explicit and shared semantics.

Although the idea is not new—similar concepts such as semantic networks, knowledge bases, ontologies, and linked data have existed since the 1980s and 1990s—the emphasis in knowledge graphs is on self-describing semantics, standardized technologies (such as RDF), and practical use at scale.

What is new about Knowledge Graphs?

nothing is fundamentally new.
The novelty is in combination and emphasis, not in invention.

Earlier concepts (80s–90s)

Concept	 :         Focus

Semanti networks:	Graphs of concepts and relations

Knowledge bases:	  Structured facts

Ontologies	  :    Formal domain models

Linked Data	   :   Web-scale linking using URIs

Knowledge Graphs emphasize:

✔ Self-describing data

✔ Explicit semantics embedded in the data

✔ Standardized, interoperable stack

✔ Operational use (analytics, AI, integration)


The “Self-Semantic” aspect (very important)

In a Knowledge Graph:

Data carries its own meaning

Meaning is not hidden in application code

Entities are typed

Relationships are named and reusable

Example:

:Alice a :Person ;

       :worksFor :Hospital_12 .


This graph is meaningful without external documentation.

That’s what “self-semantic” means.

Technology stack (what makes it practical today)

Core stack:

RDF → data model (triples)

OWL → semantics and constraints

SPARQL → querying

URIs → global identifiers

Graph databases / triple stores → scalability

This stack makes semantics:

explicit

machine-readable

interoperable

queryable

Scope: Single-domain vs Multi-domain

This is an important classification.

Single-domain Knowledge Graph

Focused on one business domain

Example: HR, healthcare, finance

Strong ontology alignment

High semantic precision

Multi-domain Knowledge Graph

Integrates multiple domains

Shared identifiers and ontologies

Cross-domain reasoning

Higher complexity

Purpose: Why build a Knowledge Graph?

Common purposes:
Purpose:	Example
Data integration:	Combine API, CSV, DB sources

Data analysis:	Indicators, reporting

AI applications:	Feature graphs, reasoning

Interoperability:	Exchange across systems

Knowledge reuse:	Shared domain models

The value of a knowledge graph depends on three crucial dimensions of meaning: accuracy, explicitness, and agreement. Accuracy ensures that the modeled entities and relationships correctly reflect the real-world domain. Explicitness ensures that meaning is directly encoded in the data and not left implicit or hidden in application logic. Agreement ensures that semantics are shared and understood consistently across systems and stakeholders, typically through standardized ontologies. Together, these dimensions enable reliable integration, analysis, and reuse.

-Meaning accuracy ensures we model the right concepts. (ontology classes)

-Meaning explicitness ensures the meaning is visible in the data itself. (properties, no hidden meaning)

-Meaning agreement ensures everyone uses the same meaning. (ontology governance, avoid custom predicates)

A knowledge graph exists only when all three are satisfied.

If one dimension is missing → the graph degrades into “just data”.

Knowledge Graph Quality Dimensions

Problems, Causes, and Detection

When developing and applying a Knowledge Graph (KG), quality issues do not come from “bad RDF syntax” — they come from semantic failures.

Below is a practical quality model centered on meaning.

A knowledge graph may be inaccurate for several reasons. Inaccuracies can arise from automatic information extraction methods that misidentify entities or relationships, from errors or inconsistencies in the underlying data sources, from misunderstandings of ontology modeling elements during the mapping process, and from insufficient domain knowledge of the modeler. These causes often interact, making accuracy a semantic challenge rather than a purely technical one.

Vagueness in a knowledge graph arises when classes or relations lack precise semantic definitions. Such vagueness enables multiple interpretations of the same graph, which in turn leads to disagreement across use cases, systems, or stakeholders. While a knowledge graph may remain technically valid, vague concepts undermine meaning agreement and result in inconsistent analytical, integrative, or regulatory outcomes. Reducing vagueness through explicit, well-defined ontology elements is therefore essential for reliable knowledge graph use.

### Incompleteness, Inconsistency, and Conciseness in Knowledge Graphs

These dimensions describe structural and semantic quality, not technology correctness.

1️⃣ Incompleteness — “Something is missing”
Definition

A Knowledge Graph is incomplete when it lacks information that is required to fulfill its intended purpose.

Incompleteness is always relative to a use case.

Examples

❌ Incomplete

:Contract_123 a onto:contract .


Missing:

start date

organization

person

This contract exists, but cannot be used meaningfully.

✅ Complete (for reporting use case)

:Contract_123 a onto:contract ;

    onto:hasemployee :Person_1 ;
    
    onto:hasorganization :Org_5 ;
    
    onto:hasstartdate "2023-01-01"^^xsd:date .

Causes of incompleteness

Unclear scope or competency questions

Partial data sources

Incremental loading without coverage checks

Missing relationships (more common than missing entities)

Detection

Competency question testing

SPARQL “missing pattern” queries:

SELECT ?c WHERE {

  ?c a onto:contract .
  
  FILTER NOT EXISTS { ?c onto:hasstartdate ?d }
  
}

2️⃣ Inconsistency — “Contradictions exist”

Definition

A Knowledge Graph is inconsistent when it contains statements that cannot all be true at the same time, given the ontology semantics.

Examples

❌ Inconsistent

:Person_1 a onto:Person .

:Person_1 a onto:Organisation .


If Persoon and Organisation are disjoint classes → inconsistency.

Another example:

:Contract_1 onto:haststartdate "2024-01-01"^^xsd:date ;

           onto:hasenddate "2023-12-31"^^xsd:date .

Causes of inconsistency

Poor data quality in source systems

Conflicting mappings

Ontology constraints ignored

Multiple teams modeling independently

Temporal logic errors

Detection

OWL reasoners

SHACL constraints

Logical SPARQL checks:

SELECT ?c WHERE {

  ?c onto:hasstartdate ?s ;
  
     onto:hasenddate ?e .
     
  FILTER (?e < ?s)
  
}

3️⃣ Conciseness — “No redundancy or noise”

Definition

A Knowledge Graph is concise when it avoids redundant, duplicated, or unnecessary statements, while preserving meaning.

Conciseness ≠ minimality

Conciseness = no unnecessary repetition

Examples

❌ Not concise (redundancy)

:Person_1 onto:hasName "Alice" .

:Person_1 onto:name "Alice" .


Same meaning, different predicates → redundancy.

Or:

:Person_1 a onto:Person .

:Person_1 a onto:Person .

✅ Concise

:Person_1 a onto:Person ;

          onto:hasName "Alice" .

Causes of non-conciseness

Multiple mappings of same field

Duplicate data ingestion

No identity resolution

Predicate overlap

Over-modeling

Detection

Duplicate triple detection

Predicate overlap analysis

Identity clustering checks

Example:

SELECT ?p (COUNT(*) AS ?cnt)
WHERE { ?s ?p ?o }
GROUP BY ?p
ORDER BY DESC(?cnt)

A knowledge graph is only valuable if it answers the right questions for the right users.
A knowledge graph may be irrelevant not because it is incorrect, but because it fails to support its intended purpose. Irrelevance often arises from unclear use cases, misaligned scope, over- or under-modeling, lack of stakeholder alignment, or absence of downstream applications. Without clearly defined competency questions and success criteria, a knowledge graph risks becoming a technically sound but practically unused artifact.

Accuracy Maintenance Loop (Mental Model)

Source Change

   ↓
   
Data Validation

   ↓
   
Semantic Validation

   ↓
   
Ontology Alignment

   ↓
   
User Feedback

   ↓
   
Correction & Documentation

Entity lexicalization is the process of associating entities in a knowledge graph with human-readable names and linguistic expressions. It enables humans and language-based systems to refer to entities using natural language while preserving stable, machine-oriented identifiers. Lexicalization supports search, interoperability, multilinguality, and user interaction without compromising semantic precision.


Ontologies and rules can be used to define and reason about the semantics of the terms used in the graph. “explicit knowledge,” i.e., something that is known and can be written down. Graphs offer a flexible way to conceptualise, represent, and integrate diverse and incomplete data. 

Resource Description Framework
(RDF) defines three types of nodes: Internationalised Resource Identifiers (IRIs),
used for globally identifying entities and relations on the Web; literals, used to represent strings
and other datatype values (integers, dates, etc.); and blank nodes, used to denote the existence of
an entity.

Classes. Often, we can group nodes in a graph into classes—such as Event, City, and so
on—with a type property.

Why and How to Use Knowledge Graphs for Enterprise Analytics & AI

1. Motivation

Enterprise data is rarely simple.

Even when data is stored in relational databases or CSV files, answering business questions often requires:

understanding implicit business concepts

combining data across many tables/files

applying domain-specific rules

handling time validity

avoiding double counting

Large Language Models (LLMs) struggle with this complexity when querying raw SQL schemas, because SQL schemas describe how data is stored, not what it means.

why Knowledge Graphs (KGs) help,

how they improve query correctness,

and how they fit into modern data & AI architectures.

2. The Core Problem with Enterprise SQL

In enterprise environments:

Schemas are large and normalized

Table and column names are technical

Business logic is spread across joins and filters

Important concepts are implicit

Example business question:

“On a given date, how many unique clients per care profile receive care at a location, broken down by delivery form?”

To answer this in SQL, you must know:

which tables represent clients, profiles, locations

how delivery forms are encoded (flags, codes, lookup tables)

how time validity is modeled

how to avoid double counting across joins

This makes queries:

long and fragile

hard to validate

difficult for LLMs to generate correctly.

3. Knowledge Graphs as a Semantic Layer

A Knowledge Graph introduces a semantic layer on top of existing data.

Key idea

Instead of querying tables, you query business concepts and relationships.

A KG uses:

RDF to represent facts as triples

ontologies to define domain concepts

SPARQL to query meaning, not storage

4. From Relational Data to Knowledge Graph
Step 1: Identify business concepts

From tables or CSVs, extract concepts such as:

Client

Location

Care Profile

Care Process

Care Indication

Delivery Form

Step 2: Make relationships explicit

Instead of foreign keys, model:

client receives care via process

process occurs at location

indication has care profile

indication has delivery form

6. Why SPARQL Is Easier Than SQL for Business Questions
7. 
SQL mindset

How are tables joined?

Which columns encode this meaning?

How do I avoid duplicates?

SPARQL mindset

Which facts must be true?

How are concepts related?

Which conditions apply?

7. Results from Research (Why This Works)

Research shows that:

LLMs perform poorly on complex enterprise SQL schemas

Accuracy drops to near zero for highly joined queries

Introducing a Knowledge Graph triples accuracy

Ontologies prevent hallucinations by constraining vocabulary

Key insight:

Context and semantics matter more than model size.









