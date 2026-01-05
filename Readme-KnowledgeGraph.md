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




