# Databricks notebook source
# MAGIC %md
# MAGIC ## a) For years 2018 and onwards

# COMMAND ----------

import re
import os
import csv

# Specify the folder path containing the .txt files
folder_path = ''

# Specify the custom path for the output CSV file
output_path = '.csv'

output_pickle_path = ''

# Initialize a list to store data (project ID and extracted text) from multiple files
data = []


def remove_TableOfContents(text):
    # Find the position of the pattern in the text
    pattern = r"Table of Contents|Contents|TABLE OF CONTENTS|CONTENTS"
    characters_to_remove = 10000
    match = re.search(pattern, text, re.IGNORECASE)
    
    # If the pattern is found, remove the specified number of characters after it
    if match:
        start_position = match.end()
        new_text = text[:start_position] + text[start_position + characters_to_remove:]
        return new_text
    else:
        return text
    
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

# Iterate over the files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(folder_path, filename)

        extracted_texts = []  # Initialize a list to store the extracted text for each file

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                text = file.read()

                # Call the function to remove lines with page numbers from the content
                text = remove_TableOfContents(text)

                # Define the start and end patterns
                extracted_text = ""
                #page_number_pattern = r'((IF ANY))'
                start_pattern4 = r"OTHER OUTCOMES AND IMPACTS|OTHER OUTCOMES AND IMPACTS|OTHER OUTCOMES AND IMPACTS (IF ANY)|E. OTHER OUTCOMES AND IMPACTS|E. OTHER OUTCOMES AND IMPACTS (IF ANY)|E\. OTHER OUTCOMES AND IMPACTS|E\. OTHER OUTCOMES AND IMPACTS (IF ANY)"
                end_pattern4 = r"II\.\s*KEY FACTORS THAT AFFECTED IMPLEMENTATION AND OUTCOME|II. KEY FACTORS THAT AFFECTED IMPLEMENTATION AND OUTCOME|III\.\s*KEY FACTORS THAT AFFECTED IMPLEMENTATION AND OUTCOME*?A\.|III\.\s*KEY FACTORSn THAT AFFECTED IMPLEMENTATION AND OUTCOME.*?A\.|IV\.\s*KEY FACTORS THAT AFFECTED IMPLEMENTATION AND OUTCOME.*?A\.|KEY FACTORS THAT AFFECTED IMPLEMENTATION AND OUTCOME*?A\.|III\.\s*IMPLEMENTATION ARRANGEMENTS.*?A\.|IV\.\s*IMPLEMENTATION ARRANGEMENTS.*?A\.|\.\s*KEY FACTORS THAT AFFECTED IMPLEMENTATION AND OUTCOME.*?A\.|2\.\s*KEY FACTORS THAT AFFECTED IMPLEMENTATION AND OUTCOME.*?A\.|3\.\s*KEY FACTORS THAT AFFECTED IMPLEMENTATION AND OUTCOME.*?A\.|4\.\s*KEY FACTORS THAT AFFECTED IMPLEMENTATION AND OUTCOME.*?A\.|3\.\s*KEY FACTORS THAT AFFECTED IMPLEMENTATION AND OUTCOME.*?A\.|4\.\s*KEY FACTORS THAT AFFECTED IMPLEMENTATION AND OUTCOME.*?A\."

                # Use regular expressions to find the text between the start and end patterns
                start_match = re.search(start_pattern4, text, re.DOTALL | re.IGNORECASE)
                end_match = re.search(end_pattern4, text, re.DOTALL | re.IGNORECASE)

                if start_match and end_match: #and start_match.start() < end_match.start():
                    start_position = start_match.end()  # End position of the start pattern
                    end_position = end_match.start()    # Start position of the end pattern

                    extracted_text = text[start_position:end_position].strip()
                    if extracted_text:
                        # Define a pattern to capture the footer notes
                        footer_patterns = [
                            r'^\d+$',
                            r'Page \d+ of \d+',
                            r'Page \d+',
                            r'The World Bank\s+(.*?)\s+\(P\d+\)',
                            r'The World Bank\s+(.*?)\s+\(\sP\d+\s\)',
                            r'(\d+)\s+of\s+(\d+)',
                            r'(())',
                            r'Gender\s+',
                            r'(IF ANY)',
                            r'(if any)',
                            r'^.{2}$'
                        ]

                        footer_pattern = re.compile('|'.join(footer_patterns), re.DOTALL)

                        # Remove footer notes
                        extracted_text = re.sub(footer_pattern, '', extracted_text)
                        #cleaned_text = re.sub(page_number_pattern, '', extracted_text)
                        cleaned_text = re.sub(r'\n+', '\n', extracted_text)
                        cleaned_text = re.sub(r'^\(\)$','',cleaned_text)
                        extracted_texts.append(cleaned_text)
                    else:
                        extracted_texts.append("N/A")
                else:
                    extracted_texts.append("N/A")

        except FileNotFoundError:
            extracted_texts.append("File not found")

        # Get the project ID for this file
        project_id = extract_project_id_from_file(file_path)

        # Append the project ID and extracted text for this file to the data list
        data.append([project_id, extracted_texts])

        
# Write the data to the CSV file
with open(output_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Project ID', 'Other Outcomes and Impacts'])
    for project_id, extracted_text_list in data:
        # Convert the extracted text list to a string
        extracted_text = "\n".join(extracted_text_list)
        # Remove lines containing only '()'
        cleaned_text = re.sub(r'^\(\)$', '', extracted_text, flags=re.MULTILINE)
        cleaned_text = re.sub(r'^I$', '', cleaned_text, flags=re.MULTILINE)
        cleaned_text = re.sub(r'\d{1,2}$', '', cleaned_text, flags=re.MULTILINE)
        csvwriter.writerow([project_id, cleaned_text])

# Write the data to the pickle file
with open(output_pickle_path, 'wb') as picklefile:
    pickle.dump(data, picklefile)

# Print a message to indicate the file has been saved
print(f'Data has been saved to {output_pickle_path}.')

# Print a message to indicate the file has been saved
print(f'Data has been saved to {output_path}')


# COMMAND ----------

# MAGIC %md
# MAGIC ## b) For years before 2018

# COMMAND ----------

import re
import os
import csv

# Specify the folder path containing the .txt files
folder_path = ''

# Specify the custom path for the output CSV file
output_path = '.csv'


output_pickle_path = ''

# Initialize a list to store data (project ID and extracted text) from multiple files
data = []

# Define a function to remove lines with page numbers from a text string
def remove_page_numbers(content_bad):
    pattern = r'^\d+$|Page \d+ of \d+'
    pattern2 = r'Page \d+'
    pattern3 = r'The World Bank\s+(.*?)\s+\(P\d+\)'  
    pattern4 = r'(\d+)\s+of\s+(\d+)'
    
   
    # Use re.MULTILINE to apply the pattern to each line in the text
    modified_text = re.sub(pattern, '', content_bad, flags=re.MULTILINE)
    modified_text2 = re.sub(pattern2, '', modified_text, flags=re.MULTILINE)   
    modified_text3 = re.sub(pattern3, '', modified_text2, flags=re.MULTILINE)
    good_text = re.sub(pattern4, '', modified_text3, flags=re.MULTILINE)
    

    return good_text


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

# Iterate over the files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(folder_path, filename)

        extracted_texts = []  # Initialize a list to store the extracted text for each file

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                text = file.read()

                # Call the function to remove lines with page numbers from the content
                text = remove_page_numbers(text)

                # Define the start and end patterns
                extracted_text = ""
                page_number_pattern = r'\b\d{1,2}\b'
                start_pattern4 = r"3.5 Overarching Themes, Other Outcomes and Impacts"
                end_pattern4 = r"3.6 Summary of Findings of Beneficiary Survey"

                start_matches = list(re.finditer(start_pattern4, text, re.DOTALL | re.IGNORECASE))
                end_matches = list(re.finditer(end_pattern4, text, re.DOTALL | re.IGNORECASE))
                
                # Check if both start and end matches were found
                if start_matches and end_matches:
                    start_position = start_matches[0].end()  # End position of the first start pattern
                    end_position = end_matches[0].start()    # Start position of the first end pattern

                    extracted_text = text[start_position:end_position].strip()
                if extracted_text:
                    cleaned_text = re.sub(page_number_pattern, '', extracted_text)
                    cleaned_text = re.sub(r'\n+', '\n', cleaned_text)
                    extracted_texts.append(cleaned_text)
                else:
                    extracted_texts.append("N/A")

        except FileNotFoundError:
            extracted_texts.append("File not found")

        # Get the project ID for this file
        project_id = extract_project_id_from_file(file_path)

        # Append the project ID and extracted text for this file to the data list
        data.append([project_id, extracted_texts])

# Write the data to the CSV file
with open(output_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Project ID', 'Other Outcomes and Impacts'])
    for project_id, extracted_text_list in data:
        # Convert the extracted text list to a string
        extracted_text = "\n".join(extracted_text_list)
        # Remove lines containing only '()'
        cleaned_text = re.sub(r'^\(\)$', '', extracted_text, flags=re.MULTILINE)
        cleaned_text = re.sub(r'^I$', '', cleaned_text, flags=re.MULTILINE)
        cleaned_text = re.sub(r'\d{1,2}$', '', cleaned_text, flags=re.MULTILINE)
        csvwriter.writerow([project_id, cleaned_text])

# Write the data to the pickle file
with open(output_pickle_path, 'wb') as picklefile:
    pickle.dump(data, picklefile)

# Print a message to indicate the file has been saved
print(f'Data has been saved to {output_pickle_path}.')

# Print a message to indicate the file has been saved
print(f'Data has been saved to {output_path}')
