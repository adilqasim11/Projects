#!/usr/bin/env python
# coding: utf-8

# ## 1) Initial extraction for Footer Notes

# In[1]:


import re
import os
import csv

csv.field_size_limit(10000000) 

# Define the folder containing the files and the output CSV file name
folder_path = '' # path containing the downloaded files
output_csv_file = '1.csv'

def extract_project_id_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            text = file.read()
            project_id_pattern = r"P\d{6}"
            project_id = re.search(project_id_pattern, text)
            
            if project_id:
                return project_id.group()
            else:
                return "N/A"
    except FileNotFoundError:
        return "File not found"

# Create a list to store all data (filename and matches)
all_data = []

# Define a function to process a single file and extract the results
def process_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
        #text2 = clean_this(text)

        pattern1 = r'(?!\d\.)\n+\s+\d{1,2}\s+[A-Z][a-zA-Z]*.*?\(P\d+\)'
        pattern4 = r'(?!\d\.)\n+\s+\d{1,2}[A-Z][a-zA-Z]*.*?\(P\d+\)'
        pattern2 = r'(?!\d\.)\n\d{1,2}\s+[A-Z][a-zA-Z]*.*?\(P\d+\)'
        pattern3 = r'(?!\d\.)\n\d{1,2}[A-Z][a-zA-Z]*.*?\(P\d+\)'
        matches1 = re.findall(pattern1, text, re.DOTALL)
        matches2 = re.findall(pattern2, text, re.DOTALL)
        matches3 = re.findall(pattern3, text, re.DOTALL)
        matches4 = re.findall(pattern4, text, re.DOTALL)

        # Combine all matches into one list
        all_matches = matches1 + matches2 + matches3 + matches4

        # Create a set to store unique matches
        unique_matches = set()

        # Patterns to remove
        remove_patterns = [
            r'^\d+$|Page \d+ of \d+',
            r'Page \d+',
            r'The World Bank\s+(.*?)\s+\(P\d+\)',
            r'(\d+)\s+of\s+(\d+)',
            r'(\n+\d{1,2}\.\s+.*?(?=\n{2,}))',
            r'(\n\d{1,2}\.\s+.*?(?=\n{2,}))',
            r'(\n+\s+\d{1,2}\.\s+.*?(?=\n{2,}))',
            r'(\n\s+\d{1,2}\.\s+.*?(?=\n{2,}))',
            r'^\s*\d{1,2}\.\s.*?(?=\n{2,})',
            #r'(\S+(?:\s{2,}\S+)+)'
        ]

        for match in all_matches:
            # Remove specified patterns
            for pattern in remove_patterns:
                match = re.sub(pattern, '', match)
            stripped_match = match.strip()
            if stripped_match and stripped_match not in unique_matches:
                # Add the stripped match to the set of unique matches
                unique_matches.add(stripped_match)
        
        # Concatenate all unique matches into a single string
        concatenated_matches = '\n'.join(unique_matches)

        # Append filename and concatenated matches to the list
        all_data.append((extract_project_id_from_file(file_path), concatenated_matches))

        

# List all files in the folder and process each one
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(folder_path, filename)
        process_file(file_path)


# Create a CSV file with two columns (filename and matches)
with open(output_csv_file, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write header row
    csv_writer.writerow(['Project_ID', 'Footer Notes'])

    # Write data to the CSV file
    csv_writer.writerows(all_data)

print(f'All data have been saved to {output_csv_file}')


# ## 2) Remove tables from the Footer Notes

# In[2]:


import re
import csv
import os

csv.field_size_limit(10000000) 
pattern_t3 = r'((?:\s{3,})+)'
patternline = re.compile(r'([a-zA-Z]+)(\d{1,2})')
#patternline = re.compile(r'([a-zA-Z]+)(?<!_)(\d{1,2})(?!_)')
#patternline = re.compile(r'([a-zA-Z]+)(?<![_/])(\d{1,2})(?![_/])')
# Function to clean the text based on the patterns

def clean_text(text):
    #text = re.sub(pattern_t2, '', text, flags=re.DOTALL)
    text = re.sub(pattern_t3, '', text, flags=re.DOTALL)
    #text = re.sub(r'\n\n', '\n', text, flags=re.DOTALL)
    #text = re.sub(patternline, r'\1\n\2', text)
    text = re.sub(r'\n\s*\n', '\n', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text


#print("Data cleaned and saved to", output_file)
input_file = '1.csv' #from previos step
output_file = '2.csv' 
# Get field names from the input file
with open(input_file, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames

# Read the data and clean it
data = []
with open(input_file, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        row['Footer Notes'] = clean_text(row['Footer Notes'])
        

        # Append the row to the data list
        data.append(row)

# Drop rows with NaN values in 'Matches' column
data = [row for row in data if row['Footer Notes']]

# Write the cleaned data to a new CSV file
with open(output_file, 'w', newline='') as cleaned_file:
    writer = csv.DictWriter(cleaned_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)


# ## 3) Extract clean Footer Notes

# In[3]:


import re
import csv

# Open the input CSV file for reading
input_file = '2.csv' #previous step file
output_file = 'FooterNotes.csv'

import spacy
csv.field_size_limit(10000000) 


def clean_text(paragraphs):
    paragraphs = paragraphs.split('\n')
    # Remove duplicate paragraphs
    paragraphs = list(set(paragraphs))

    # Remove paragraphs with just one or two digit numbers and the rest empty
    paragraphs = [p for p in paragraphs if not re.match(r'^\s*\d{1,2}\s*$', p)]

    # Sort paragraphs in numerical order based on the starting single or two digit number
    paragraphs.sort(key=lambda x: int(re.match(r'^\d{1,2}', x).group()) if re.match(r'^\d{1,2}', x) else float('inf'))

    # Add a blank line between paragraphs
    result = '\n\n'.join(paragraphs)

    return result
def remove_line_breaks_and_spaces(text):
    # Preserve blank lines between paragraphs
    paragraphs = text.split('\n\n')
    
    # Process each paragraph individually
    cleaned_paragraphs = []
    for paragraph in paragraphs:
        # Replace line breaks with a single space and remove extra white spaces within each paragraph
        cleaned_paragraph = re.sub(r'\s+', ' ', paragraph).strip()
        cleaned_paragraphs.append(cleaned_paragraph)

    # Join the cleaned paragraphs with two newline characters
    cleaned_text = '\n\n'.join(cleaned_paragraphs)

    return cleaned_text

def distribute_paragraphs(text):
    # Load spaCy NER model
    nlp = spacy.load("en_core_web_sm")

    # Process the text
    doc = nlp(text)

    # Initialize variables
    current_paragraph = []
    paragraphs = []

    for token in doc:
        # Check if the token is a cardinal number of one or two digits
        if re.match(r'^\d{1,2}|^\s*\d{1,2}\s*[A-Z][a-zA-Z].*|[A-Z][a-zA-Z]\d{1,2}\s*[A-Z][a-zA-Z].*', token.text):
            # If the current paragraph is not empty, add it to the list
            if current_paragraph:
                paragraphs.append(' '.join(current_paragraph))
                current_paragraph = []  # Reset the current paragraph
        # Add the token to the current paragraph
        current_paragraph.append(token.text)

    # Add the last paragraph if the text ends with a cardinal number
    if current_paragraph:
        paragraphs.append(' '.join(current_paragraph))

    # Format each paragraph on a new line, with an additional space for non-cardinal paragraphs
    formatted_paragraphs = []
    for i, paragraph in enumerate(paragraphs):
        # Check if the paragraph starts with a non-cardinal number
        if i > 0 and not re.match(r'^\d{1,2}|^\s*\d{1,2}\s*[A-Z][a-zA-Z].*|[A-Z][a-zA-Z]\d{1,2}\s*[A-Z][a-zA-Z].*', paragraph):
            formatted_paragraphs.append('\n' + paragraph)
        else:
            formatted_paragraphs.append(paragraph)

    result_text = '\n'.join(formatted_paragraphs)

    return result_text

# Example text
# Get field names from the input file
with open(input_file, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames

# Read the data and clean it
data = []
with open(input_file, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        row['Footer Notes'] = distribute_paragraphs(str(row['Footer Notes']))
        row['Footer Notes'] = remove_line_breaks_and_spaces(str(row['Footer Notes']))
        row['Footer Notes'] = clean_text(row['Footer Notes'])
        data.append(row)

# Write the cleaned data to a new CSV file
with open(output_file, 'w', newline='') as cleaned_file:
    writer = csv.DictWriter(cleaned_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
    


print("Data cleaned and saved to", output_file)
# Distribute and join paragraphs based on cardinals and additional space for non-cardinal paragraphs


# ## 4) Extract References 

# In[4]:


import re
import csv
import argparse
import pickle

csv.field_size_limit(10000000) 
# Open the input CSV file for reading
# Define file paths
INPUT_FILE = '/FooterNotes.csv' #From previos step
OUTPUT_FILE = 'References.csv' #specify path for output
PICKLE_FILE = 'References.pkl'  # Path for pickle output



import spacy



def remove_line_breaks_and_spaces(text):
    # Preserve blank lines between paragraphs
    paragraphs = text.split('\n\n')
    
    # Process each paragraph individually
    cleaned_paragraphs = []
    for paragraph in paragraphs:
        # Replace line breaks with a single space and remove extra white spaces within each paragraph
        cleaned_paragraph = re.sub(r'\s+', ' ', paragraph).strip()
        cleaned_paragraphs.append(cleaned_paragraph)

    # Join the cleaned paragraphs with two newline characters
    cleaned_text = '\n\n'.join(cleaned_paragraphs)

    return cleaned_text

def calculate_entity_ratios(text):
    # Load the spaCy English model
    nlp = spacy.load("en_core_web_sm")

    # Process the text using spaCy
    doc = nlp(text)

    # Initialize counts for different entity types and total words
    entity_counts = {"PERSON": 0, "ORG": 0, "DATE": 0, "URL": 0}
    total_words = len(doc) if len(doc) > 0 else 1  # Avoid division by zero

    # Regular expression to identify URLs
    url_pattern = re.compile(r'https://\S+')

    # Count entities, including the custom "URL" entity
    for ent in doc.ents:
        if ent.label_ in entity_counts:
            entity_counts[ent.label_] += 1
        elif url_pattern.match(ent.text):
            entity_counts["URL"] += 1

    # Calculate ratios
    entity_ratios = {label: count / total_words for label, count in entity_counts.items()}

    return entity_ratios

def is_reference(paragraph, threshold=0.135):
    # Load the spaCy English model
    nlp = spacy.load("en_core_web_sm")

    # Process the paragraph using spaCy
    doc = nlp(paragraph)

    # Check if there are no words in the paragraph
    if len(doc) == 0:
        return False

    # Calculate the ratio of NER to words
    ner_count = sum(1 for ent in doc.ents if ent.label_ != '')
    total_words = len(doc)
    ratio = ner_count / total_words

    # Return True if the ratio is above the threshold, indicating a potential reference
    return ratio > threshold

def find_optimal_threshold(text):
    # Split the text into paragraphs
    paragraphs = text.split('\n\n')

    # Experiment with different threshold values
    references = ""
    for threshold in [0.135]:
        references += "\n"
        for i, reference in enumerate(paragraphs, start=1):
            if is_reference(reference, threshold):
                references += f"\n{reference}\n"
        references += "\n"
    print (references)
    new = remove_line_breaks_and_spaces(references.strip())
    return new

def process_references_in_csv(file_path):
    # Read data from CSV file
    data = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['Footer Notes'] = find_optimal_threshold(str(row['Footer Notes']))
            data.append(row)
    return data

def write_processed_csv(file_path, data, fieldnames):
    # ... (unchanged)
    with open(file_path, 'w', newline='') as cleaned_file:
        writer = csv.DictWriter(cleaned_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

# Function to save data to a pickle file
def save_to_pickle(file_path, data):
    with open(file_path, 'wb') as pkl_file:
        pickle.dump(data, pkl_file)

if __name__ == "__main__":
    # Get field names from the input file
    with open(INPUT_FILE, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames

    # Process the data
    processed_data = process_references_in_csv(INPUT_FILE)

    # Write the processed data to a new CSV file and a pickle file
    write_processed_csv(OUTPUT_FILE, processed_data, fieldnames)
    save_to_pickle(PICKLE_FILE, processed_data)

    print("Data processed and saved to", OUTPUT_FILE)


# In[ ]:




