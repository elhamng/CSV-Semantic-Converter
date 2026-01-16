from rdflib import Namespace

# Define common namespace URIs
#version = 3.0.0
#<owl:versionIRI rdf:resource="http://purl.org/ozo/onz-pers#/3.0.0"/>
#<owl:versionIRI rdf:resource="http://purl.org/ozo/onz-g#2.8.1"/>
#<owl:versionIRI rdf:resource="http://purl.org/ozo/onz-org#2.4.0"/>




default_s = 'http://data.example.com#'
default_ns = Namespace(default_s)
onto_s = 'http://purl.org/onto#'
onto_ns = Namespace(onto_s)
# Add Time namespace for temporal data
time_s = 'http://www.w3.org/2006/time#'
time_ns = Namespace(time_s)


NAMESPACES = {
    "": default_ns,
    "onto": onto_ns,
    "time": time_ns,
}