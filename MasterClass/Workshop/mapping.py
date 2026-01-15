import rdflib
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import RDFS, XSD
import pandas as pd
import os
from pathlib import Path


# Define common namespace URIs
#version = 3.0.0
schema = Namespace('https://schema.org/#')
ex = Namespace('http://example.org/id#')

g = rdflib.Graph()


# Bind the namespace as the default namespace
g.bind("schema", schema)
g.bind("ex", ex)

# Method 1: Using os.path.join() (recommended for cross-platform compatibility)
# For the Python-Workshop directory (if it exists)
#path = os.path.join("c:", "RDFMapping", "Python-Workshop")
#file_path = os.path.join(path, "people.csv")

#df_people = pd.read_csv(file_path, sep= ";")
#print(df_people.head())
csv_directory = "c:/RDFMapping/Python-Workshop"
person_csv = os.path.join(csv_directory, "people.csv")
events_csv = os.path.join(csv_directory,"events.csv")
df_people = pd.read_csv(person_csv , sep= ";")
print(df_people.head())

df_events= pd.read_csv(events_csv,sep=";")
print(df_events.head())


headers = df_people.columns.tolist()
for index, row in df_people.iterrows():
    try:
        # Validate required fields exist
        if pd.isna(row['name']):
            print(f"Row {index} skipped: 'name' missing.")
            continue

        person_uri = ex[f"person/{row['id']}"]
        g.add((person_uri, RDF.type, schema.Person))
        g.add((person_uri, schema.name, Literal(row["name"])))
        g.add((person_uri, schema.email, Literal(row["email"])))
        g.add((person_uri, schema.birthDate, Literal(row["birthdate"], datatype=XSD.date)))
        print(f"Processed row {index} successfully.")
        
              
    except Exception as e:
        print(f"Error processing row {index}: {e}")

headers= df_events.columns.tolist()
for index, row in df_events.iterrows():
    try:
        # Validate required fields exist
        if pd.isna(row['title']):
            print(f"Row {index} skipped: 'title' missing.")
            continue

        event_uri = URIRef(f"{ex}event_{row['event_id']}")
        g.add((event_uri, RDF.type, schema.Event))
        g.add((event_uri, schema.name, Literal(row["title"])))
        g.add((event_uri, schema.startDate, Literal(row["date"], datatype=XSD.date)))

        organiser_uri = ex[f"person/{row['organiser_id']}"]
        g.add((event_uri, schema.organizer, organiser_uri))
        print(f"Processed row {index} successfully.")
        
              
    except Exception as e:
        print(f"Error processing row {index}: {e}")      
# Save the RDF graph to a TTL file
output_file = os.path.join(csv_directory,"events_data.ttl")
g.serialize(destination=output_file, format='turtle')
print(f"RDF graph saved to {output_file}")

# Optional: Print the TTL content to see what was generated
print("\nGenerated TTL content:")
print(g.serialize(format='turtle'))