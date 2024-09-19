# Databricks notebook source
# MAGIC %md
# MAGIC ## Run this for files 19-23 (onwards)

# COMMAND ----------

import re
import os
import csv

# Specify the folder path containing the .txt files
folder_path = ''

# Specify the custom path for the output pickle file. Make sure its in ".csv" format
output_path = '.csv'# Initialize a list to store data (project ID and extracted text) from multiple files
output_pickle_path = '.pickle'

data = []



def remove_TableOfContents(text):
    # Find the position of the pattern in the text
    pattern = r"Table of Contents|Contents|TABLE OF CONTENTS|CONTENTS"
    characters_to_remove = 30000
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

                extracted_text = ""
                text_2 = ""
                start_pattern2 = r"A\.\s+Project\s+Components|B\.\s+Project\s+Components|C\.\s+Project\s+Components"
                end_pattern2 = r"B\.\s+Project\s+Cost\s+and\s+Financing"
                 # Use regular expressions to find the text between the start and end patterns
                start_match = re.search(start_pattern2, text, re.DOTALL | re.IGNORECASE)
                end_match = re.search(end_pattern2, text, re.DOTALL | re.IGNORECASE)

                if start_match and end_match:
                    start_position = start_match.end()  # End position of the start pattern
                    end_position = end_match.start()    # Start position of the end pattern

                    extracted_text = text[start_position:end_position].strip()
                    extracted_text = re.sub(r'\n{3,}', '\n', extracted_text)
                    text_2 = extracted_text
                    
    
                else:
                    start_pattern2 = r"A\.\s+Project\s+Components|B\.\s+Project\s+Components|C\.\s+Project\s+Components|B\.\s+Project\s+Financing\s+and\s+Components|B\.\s+Project\s+Description\s+and\s+Components"
                    end_pattern2 = r"B\.\s+Project\s+Beneficiaries|C\.\s+Project\s+Beneficiaries|D\.\s+Project\s+Beneficiaries|B. Project Cost and Financing|C. Project Summary Cost and Financing"
                     # Use regular expressions to find the text between the start and end patterns
                    start_match = re.search(start_pattern2, text, re.DOTALL | re.IGNORECASE)
                    end_match = re.search(end_pattern2, text, re.DOTALL | re.IGNORECASE)

                    if start_match and end_match:
                        start_position = start_match.end()  # End position of the start pattern
                        end_position = end_match.start()    # Start position of the end pattern

                        extracted_text = text[start_position:end_position].strip()
                        extracted_text = re.sub(r'\n{3,}', '\n', extracted_text)
                        text_2 = extracted_text
                    else:
                        start_pattern2 = r"A. Project Components"
                        end_pattern2 = r"B. Project Financing"
                         # Use regular expressions to find the text between the start and end patterns
                        start_match = re.search(start_pattern2, text, re.DOTALL | re.IGNORECASE)
                        end_match = re.search(end_pattern2, text, re.DOTALL | re.IGNORECASE)

                        if start_match and end_match:
                            start_position = start_match.end()  # End position of the start pattern
                            end_position = end_match.start()    # Start position of the end pattern

                            extracted_text = text[start_position:end_position].strip()
                            extracted_text = re.sub(r'\n{3,}', '\n', extracted_text)
                            text_2 = extracted_text
                            
                        else:  
                            start_pattern2 = r"A. Project Components|A.    Project Components|A.            PROJECT COMPONENTS|Project Components*?A\.|A\.\s*Project Components*?A\.|A\. Project Components"
                            end_pattern2 = r"Project Cost and Financing|B.   Project Financing|B.      PROJECT FINANCING|B. Project Financing|a. Project Financing|B\.\s*Project Financing|B\. Project Financing"
                             # Use regular expressions to find the text between the start and end patterns
                            start_match = re.search(start_pattern2, text, re.DOTALL | re.IGNORECASE)
                            end_match = re.search(end_pattern2, text, re.DOTALL | re.IGNORECASE)

                            if start_match and end_match:
                                start_position = start_match.end()  # End position of the start pattern
                                end_position = end_match.start()    # Start position of the end pattern

                                extracted_text = text[start_position:end_position].strip()
                                extracted_text = re.sub(r'\n{3,}', '\n', extracted_text)
                                text_2 = extracted_text

                                
                            else:
                                start_pattern2 = r"A. Project Components|Project Components*?A\.|A\.\s*Project Components*?A\.|A\. Project Components"
                                end_pattern2 = r"B. Project Financing|a. Project Financing|B\.\s*Project Financing|B\. Project Financing"
                                 # Use regular expressions to find the text between the start and end patterns
                                start_match = re.search(start_pattern2, text, re.DOTALL | re.IGNORECASE)
                                end_match = re.search(end_pattern2, text, re.DOTALL | re.IGNORECASE)

                                if start_match and end_match:
                                    start_position = start_match.end()  # End position of the start pattern
                                    end_position = end_match.start()    # Start position of the end pattern

                                    extracted_text = text[start_position:end_position].strip()
                                    extracted_text = re.sub(r'\n{3,}', '\n', extracted_text)
                                    text_2 = extracted_text

                            
                            

            

        except FileNotFoundError:
            extracted_texts.append("File not found")
        

        # Get the project ID for this file
        project_id = extract_project_id_from_file(file_path)
        
        footer_patterns = [
                            r'(?!\d\.)\n+\s+\d{1,2}\s+[A-Z][a-zA-Z]*.*?\(P\d+\)',
                            r'(?!\d\.)\n+\s+\d{1,2}[A-Z][a-zA-Z]*.*?\(P\d+\)',
                            r'(?!\d\.)\n\d{1,2}\s+[A-Z][a-zA-Z]*.*?\(P\d+\)',
                            r'(?!\d\.)\n+\d{1,2}\s+[A-Z][a-zA-Z]*.*?\(P\d+\)',
                            r'(?!\d\.)\n+\d{1,2}\s+[A-Z][a-zA-Z]*.*?\(P\d+\)',
                            r'(?!\d\.)\n\d{1,2}[A-Z][a-zA-Z]*.*?\(P\d+\)',
                            r'(?!\d\.)\n+\d{1,2}[A-Z][a-zA-Z]*.*?\(P\d+\)',
                          ]
        footer_patterns2 = [
                            r'^\d+$',
                            r'Page \d+ of \d+',
                            r'Page \d+',
                            r'The World Bank\s+(.*?)\s+\(P\d+\)',
                            r'The World Bank\s+(.*?)\s+\(\sP\d+\s\)',
                            r'(\d+)\s+of\s+(\d+)'
                          ]

        footer_pattern = re.compile('|'.join(footer_patterns), re.DOTALL)
        footer_pattern_again = re.compile('|'.join(footer_patterns2), re.DOTALL)
        text_2 = re.sub(footer_pattern, '', text_2)
        text_2 = re.sub(footer_pattern_again, '', text_2)
        
        if not text_2:
            text_2 = "Project Components Not Found"

        # Append the project ID and extracted text for this file to the data list
        data.append([project_id, text_2])

        
# Write the data to the CSV file
with open(output_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['project_id','Project Components'])
    csvwriter.writerows(data)

# Write the data to the pickle file
with open(output_pickle_path, 'wb') as picklefile:
    pickle.dump(data, picklefile)

# Print a message to indicate the file has been saved
print(f'Data has been saved to {output_pickle_path}.')

# Print a message to indicate the file has been saved
print(f'Data has been saved to {output_path}')


# COMMAND ----------

# MAGIC %md
# MAGIC ## Run this for files 13-18 (inclusive 18)

# COMMAND ----------

import re
import os
import csv

# Specify the folder path containing the .txt files
folder_path = ''

# Specify the custom path for the output pickle file. Make sure its in ".csv" format
output_path = '.csv'
output_pickle_path = '.pickle'

# Initialize a list to store data (project ID and extracted text) from multiple files
data = []


def remove_TableOfContents(text):
    # Find the position of the pattern in the text
    pattern = r"Table of Contents|Contents|TABLE OF CONTENTS|CONTENTS"
    characters_to_remove = 30000
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

                extracted_text = ""
                text_2 = ""
                start_pattern2 = r"A\.\s+Project\s+Components|B\.\s+Project\s+Components|C\.\s+Project\s+Components"
                end_pattern2 = r"B\.\s+Project\s+Cost\s+and\s+Financing|B\.\s+Project\s+Financing|C\.\s+Project\s+Financing|D\.\s+Project\s+Financing"
                 # Use regular expressions to find the text between the start and end patterns
                start_match = re.search(start_pattern2, text, re.DOTALL | re.IGNORECASE)
                end_match = re.search(end_pattern2, text, re.DOTALL | re.IGNORECASE)

                if start_match and end_match:
                    start_position = start_match.end()  # End position of the start pattern
                    end_position = end_match.start()    # Start position of the end pattern

                    extracted_text = text[start_position:end_position].strip()
                    extracted_text = re.sub(r'\n{3,}', '\n', extracted_text)
                    text_2 = extracted_text
    
                else:
                    start_pattern2 = r"A\.\s+Project\s+Components|B\.\s+Project\s+Components|C\.\s+Project\s+Components"
                    end_pattern2 = r"B\.\s+Project\s+Cost\s+and\s+Financing"
                     # Use regular expressions to find the text between the start and end patterns
                    start_match = re.search(start_pattern2, text, re.DOTALL | re.IGNORECASE)
                    end_match = re.search(end_pattern2, text, re.DOTALL | re.IGNORECASE)

                    if start_match and end_match:
                        start_position = start_match.end()  # End position of the start pattern
                        end_position = end_match.start()    # Start position of the end pattern

                        extracted_text = text[start_position:end_position].strip()
                        extracted_text = re.sub(r'\n{3,}', '\n', extracted_text)
                        text_2 = extracted_text                       

                    else:
                        start_pattern2 = r"A\.\s+Project\s+Components|B\.\s+Project\s+Components|C\.\s+Project\s+Components|B\.\s+Project\s+Financing\s+and\s+Components|B\.\s+Project\s+Description\s+and\s+Components"
                        end_pattern2 = r"B\.\s+Project\s+Beneficiaries|C\.\s+Project\s+Beneficiaries|D\.\s+Project\s+Beneficiaries|B. Project Cost and Financing|C. Project Summary Cost and Financing"
                         # Use regular expressions to find the text between the start and end patterns
                        start_match = re.search(start_pattern2, text, re.DOTALL | re.IGNORECASE)
                        end_match = re.search(end_pattern2, text, re.DOTALL | re.IGNORECASE)

                        if start_match and end_match:
                            start_position = start_match.end()  # End position of the start pattern
                            end_position = end_match.start()    # Start position of the end pattern

                            extracted_text = text[start_position:end_position].strip()
                            extracted_text = re.sub(r'\n{3,}', '\n', extracted_text)
                            text_2 = extracted_text
                            
                        else:
                            start_pattern2 = r"A. Project Components"
                            end_pattern2 = r"B. Project Financing"
                             # Use regular expressions to find the text between the start and end patterns
                            start_match = re.search(start_pattern2, text, re.DOTALL | re.IGNORECASE)
                            end_match = re.search(end_pattern2, text, re.DOTALL | re.IGNORECASE)

                            if start_match and end_match:
                                start_position = start_match.end()  # End position of the start pattern
                                end_position = end_match.start()    # Start position of the end pattern

                                extracted_text = text[start_position:end_position].strip()
                                #text_2 = extracted_text
                                if extracted_text:
                                    extracted_text = re.sub(r'\n{3,}', '\n', extracted_text)
                                    text_2 = extracted_text
                            else:  
                                start_pattern2 = r"A. Project Components|A.    Project Components|A.            PROJECT COMPONENTS|Project Components*?A\.|A\.\s*Project Components*?A\.|A\. Project Components"
                                end_pattern2 = r"Project Cost and Financing|B.   Project Financing|B.      PROJECT FINANCING|B. Project Financing|a. Project Financing|B\.\s*Project Financing|B\. Project Financing"
                                 # Use regular expressions to find the text between the start and end patterns
                                start_match = re.search(start_pattern2, text, re.DOTALL | re.IGNORECASE)
                                end_match = re.search(end_pattern2, text, re.DOTALL | re.IGNORECASE)

                                if start_match and end_match:
                                    start_position = start_match.end()  # End position of the start pattern
                                    end_position = end_match.start()    # Start position of the end pattern

                                    extracted_text = text[start_position:end_position].strip()
                                    extracted_text = re.sub(r'\n{3,}', '\n', extracted_text)
                                    text_2 = extracted_text
                                else:
                                    start_pattern2 = r"A. Project Components|Project Components*?A\.|A\.\s*Project Components*?A\.|A\. Project Components"
                                    end_pattern2 = r"B. Project Financing|a. Project Financing|B\.\s*Project Financing|B\. Project Financing"
                                     # Use regular expressions to find the text between the start and end patterns
                                    start_match = re.search(start_pattern2, text, re.DOTALL | re.IGNORECASE)
                                    end_match = re.search(end_pattern2, text, re.DOTALL | re.IGNORECASE)

                                    if start_match and end_match:
                                        start_position = start_match.end()  # End position of the start pattern
                                        end_position = end_match.start()    # Start position of the end pattern

                                        extracted_text = text[start_position:end_position].strip()
                                        extracted_text = re.sub(r'\n{3,}', '\n', extracted_text)
                                        text_2 = extracted_text

                            
                            

        except FileNotFoundError:
            extracted_texts.append("File not found")

        # Get the project ID for this file
        project_id = extract_project_id_from_file(file_path)
        
        footer_patterns = [
                            r'(?!\d\.)\n+\s+\d{1,2}\s+[A-Z][a-zA-Z]*.*?\(P\d+\)',
                            r'(?!\d\.)\n+\s+\d{1,2}[A-Z][a-zA-Z]*.*?\(P\d+\)',
                            r'(?!\d\.)\n\d{1,2}\s+[A-Z][a-zA-Z]*.*?\(P\d+\)',
                            r'(?!\d\.)\n+\d{1,2}\s+[A-Z][a-zA-Z]*.*?\(P\d+\)',
                            r'(?!\d\.)\n+\d{1,2}\s+[A-Z][a-zA-Z]*.*?\(P\d+\)',
                            r'(?!\d\.)\n\d{1,2}[A-Z][a-zA-Z]*.*?\(P\d+\)',
                            r'(?!\d\.)\n+\d{1,2}[A-Z][a-zA-Z]*.*?\(P\d+\)',
                          ]
        footer_patterns2 = [
                            r'^\d+$',
                            r'\n\d+\n',
                            r'\s{3,}\d+\s{3,}',
                            r'Page \d+ of \d+',
                            r'Page \d+',
                            r'The World Bank\s+(.*?)\s+\(P\d+\)',
                            r'The World Bank\s+(.*?)\s+\(\sP\d+\s\)',
                            r'(\d+)\s+of\s+(\d+)'
                          ]

        footer_pattern = re.compile('|'.join(footer_patterns), re.DOTALL)
        footer_pattern_again = re.compile('|'.join(footer_patterns2), re.DOTALL)
        text_2 = re.sub(footer_pattern, '', text_2)
        text_2 = re.sub(footer_pattern_again, '', text_2)
        
        if not text_2:
            text_2 = "Project Components Not Found"

        # Append the project ID and extracted text for this file to the data list
        data.append([project_id, text_2])

        
# Write the data to the CSV file
with open(output_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['project_id','Project Components'])
    csvwriter.writerows(data)

# Write the data to the pickle file
with open(output_pickle_path, 'wb') as picklefile:
    pickle.dump(data, picklefile)

# Print a message to indicate the file has been saved
print(f'Data has been saved to {output_pickle_path}.')

# Print a message to indicate the file has been saved
print(f'Data has been saved to {output_path}')


# COMMAND ----------

