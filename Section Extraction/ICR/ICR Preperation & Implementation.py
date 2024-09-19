# Databricks notebook source
# MAGIC %md
# MAGIC ## 2018-2023

# COMMAND ----------

"""
Run this part for extracting Preperation and Implementaion in a pickle file from the files from year 2018 to 2023(included)
"""

import re
import os
import pickle

# Specify the folder path containing the .txt files
folder_path = ''

# Specify the custom path for the output pickle file
output_pickle_path =  '.pkl'

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

                # Define the start and end patterns
                extracted_text = ""
                text_1 = ""

                start_pattern1 = r"3.1 KEY FACTORS DURING PREPARATION"
                end_pattern1 = r"3.2 KEY FACTORS DURING IMPLEMENTATION"

                        # Use regular expressions to find the text between the start and end patterns
                start_match = re.search(start_pattern1, text, re.DOTALL | re.IGNORECASE)
                end_match = re.search(end_pattern1, text, re.DOTALL | re.IGNORECASE)

                if start_match and end_match: #and start_match.start() < end_match.start():
                    start_position = start_match.end()  # End position of the start pattern
                    end_position = end_match.start()    # Start position of the end pattern
                
                    extracted_text = text[start_position:end_position].strip()
                    extracted_text = re.sub(r'\n{3,}', '\n', extracted_text)
                    text_1 = extracted_text

                else:

                    start_pattern1 = r"A. KEY FACTORS DURING PREPARATION"
                    end_pattern1 = r"B. KEY FACTORS DURING IMPLEMENTATION"

                            # Use regular expressions to find the text between the start and end patterns
                    start_match = re.search(start_pattern1, text, re.DOTALL | re.IGNORECASE)
                    end_match = re.search(end_pattern1, text, re.DOTALL | re.IGNORECASE)

                    if start_match and end_match: #and start_match.start() < end_match.start():
                        start_position = start_match.end()  # End position of the start pattern
                        end_position = end_match.start()    # Start position of the end pattern

                        extracted_text = text[start_position:end_position].strip()
                        extracted_text = re.sub(r'\n{3,}', '\n', extracted_text)
                        text_1 = extracted_text

                    else:
                        start_pattern1 = r"2.1 Project Preparation, Design and Quality at Entry|  A. KEY FACTORS DURING PREPARATION"
                        end_pattern1 = r"2.2 Implementation|  B. KEY FACTORS DURING IMPLEMENTATION"

                                # Use regular expressions to find the text between the start and end patterns
                        start_match = re.search(start_pattern1, text, re.DOTALL | re.IGNORECASE)
                        end_match = re.search(end_pattern1, text, re.DOTALL | re.IGNORECASE)

                        if start_match and end_match: #and start_match.start() < end_match.start():
                            start_position = start_match.end()  # End position of the start pattern
                            end_position = end_match.start()    # Start position of the end pattern

                            extracted_text = text[start_position:end_position].strip()
                            extracted_text = re.sub(r'\n{3,}', '\n', extracted_text)
                            text_1 = extracted_text
                        else:
                            start_pattern1 = r" A. KEY FACTORS DURING PREPARATION|III.A. Key Factors during Preparation |A. Key Factors During Project Preparation|\s+ KEY FACTORS DURING PREPARATION|KEY FACTORS DURING PREPARATION|FACTORS DURING PREPARATION|A. KEY FACTORS DURING PREPARATION |A. KEY FACTORS DURING PREPARATION"
                            end_pattern1 = r" B. KEY FACTORS DURING IMPLEMENTATION|III.B. Key Factors during Implementation|    B. Key Factors During Project Implementation|\s+ KEY FACTORS DURING IMPLEMENTATION|KEY FACTORS DURING IMPLEMENTATION|FACTORS DURING IMPLEMENTATION|B. KEY FACTORS DURING IMPLEMENTATION|B. KEY FACTORS DURING IMPLEMENTATION"

                                    # Use regular expressions to find the text between the start and end patterns
                            start_match = re.search(start_pattern1, text, re.DOTALL | re.IGNORECASE)
                            end_match = re.search(end_pattern1, text, re.DOTALL | re.IGNORECASE)

                            if start_match and end_match: #and start_match.start() < end_match.start():
                                start_position = start_match.end()  # End position of the start pattern
                                end_position = end_match.start()    # Start position of the end pattern

                                extracted_text = text[start_position:end_position].strip()
                                extracted_text = re.sub(r'\n{3,}', '\n', extracted_text)
                                text_1 = extracted_text
                            else:
                                text_1 = "N/A"


                extracted_text = ""
                text_2 = ""

                start_pattern2 = r"3.2 KEY FACTORS DURING IMPLEMENTATION"
                end_pattern2 = r"3.3 FACTORS SUBJECT TO WORLD BANK CONTROL"
                # Use regular expressions to find the text between the start and end patterns
                start_match = re.search(start_pattern2, text, re.DOTALL | re.IGNORECASE)
                end_match = re.search(end_pattern2, text, re.DOTALL | re.IGNORECASE)

                if start_match and end_match: #and start_match.start() < end_match.start():
                    start_position = start_match.end()  # End position of the start pattern
                    end_position = end_match.start()    # Start position of the end pattern

                    extracted_text = text[start_position:end_position].strip()
                    extracted_text = re.sub(r'\n{3,}', '\n', extracted_text)
                    text_2 = extracted_text

                else:
                    start_pattern2 = r"B. KEY FACTORS DURING IMPLEMENTATION"
                    end_pattern2 = r"IV. BANK PERFORMANCE, COMPLIANCE ISSUES, AND RISK TO DEVELOPMENT OUTCOME"
                    # Use regular expressions to find the text between the start and end patterns
                    start_match = re.search(start_pattern2, text, re.DOTALL | re.IGNORECASE)
                    end_match = re.search(end_pattern2, text, re.DOTALL | re.IGNORECASE)

                    if start_match and end_match: #and start_match.start() < end_match.start():
                        start_position = start_match.end()  # End position of the start pattern
                        end_position = end_match.start()    # Start position of the end pattern

                        extracted_text = text[start_position:end_position].strip()
                        extracted_text = re.sub(r'\n{3,}', '\n', extracted_text)
                        text_2 = extracted_text

                    else:       
                        start_pattern2 = r"Key factors during Implementation|2.2 Major Factors Affecting Implementation| B. KEY FACTORS DURING IMPLEMENTATION"
                        end_pattern2 = r"Quality of Monitoring and Evaluation|2.3 Monitoring and Evaluation| IV. BANK PERFORMANCE, COMPLIANCE ISSUES, AND RISK TO DEVELOPMENT OUTCOME "
                        # Use regular expressions to find the text between the start and end patterns
                        start_match = re.search(start_pattern2, text, re.DOTALL | re.IGNORECASE)
                        end_match = re.search(end_pattern2, text, re.DOTALL | re.IGNORECASE)

                        if start_match and end_match: #and start_match.start() < end_match.start():
                            start_position = start_match.end()  # End position of the start pattern
                            end_position = end_match.start()    # Start position of the end pattern

                            extracted_text = text[start_position:end_position].strip()
                            extracted_text = re.sub(r'\n{3,}', '\n', extracted_text)
                            text_2 = extracted_text

                        else:
                            start_pattern2 = r"The following factors affected implementation:|B. KEY FACTORS DURING IMPLEMENTATION|2.2 Implementation|Project implementation was affected by several factors, including the following:|2.2 Major Factors Affecting Implementation:|III.B. Key Factors during Implementation|    B. Key Factors During Project Implementation|\s+ KEY FACTORS DURING IMPLEMENTATION|KEY FACTORS DURING IMPLEMENTATION|B. KEY FACTORS DURING IMPLEMENTATION|2.2     Major Factors Affecting Implementation|FACTORS DURING IMPLEMENTATION|2.1 Major Factors Affecting Implementation"
                            end_pattern2 = r"IV. BANK PERFORMANCE, COMPLIANCE ISSUES, AND RISK TO DEVELOPMENT |2.3 Monitoring and Evaluation \(M&E\) Design, Implementation and Utilization|C. Factors Subject to World Bank Control|  IV.     BANK PERFORMANCE, COMPLIANCE ISSUES, AND RISK TO DEVELOPMENT OUTCOME|2.2 Monitoring and Evaluation \(M&E\) Design, Implementation and Utilization|2.3     Monitoring and Evaluation \(M&E\) Design, Implementation and Utilization|BANK PERFORMANCE, COMPLIANCE ISSUES, AND RISK TO DEVELOPMENT OUTCOME|IV.       BANK PERFORMANCE, COMPLIANCE ISSUES, AND RISK TO DEVELOPMENT OUTCOME "
                                    # Use regular expressions to find the text between the start and end patterns
                            start_match = re.search(start_pattern2, text, re.DOTALL | re.IGNORECASE)
                            end_match = re.search(end_pattern2, text, re.DOTALL | re.IGNORECASE)

                            if start_match and end_match: #and start_match.start() < end_match.start():
                                start_position = start_match.end()  # End position of the start pattern
                                end_position = end_match.start()    # Start position of the end pattern

                                extracted_text = text[start_position:end_position].strip()
                                extracted_text = re.sub(r'\n{3,}', '\n', extracted_text)
                                text_2 = extracted_text
                            else:
                                text_2 = "N/A"
                                
        except FileNotFoundError:
            extracted_texts.append("File not found")

        # Get the project ID for this file
        project_id = extract_project_id_from_file(file_path)
        
        footer_patterns = [
                            r'(?!\d\.)\n+\s+\d{1,2}\s+[A-Z][a-zA-Z]*.*?\(P\d+\)',
                            r'IV. BANK PERFORMANCE, COMPLIANCE ISSUES, AND RISK TO DEVELOPMENT OUTCOME',
                            r'IV\.\s+BANK PERFORMANCE, COMPLIANCE ISSUES, AND RISK TO DEVELOPMENT OUTCOME',
                            r'BANK PERFORMANCE, COMPLIANCE ISSUES, AND RISK TO DEVELOPMENT OUTCOME',
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
        
        text_1 = re.sub(footer_pattern, '', text_1)
        text_1 = re.sub(footer_pattern_again, '', text_1)

        # Append the project ID and extracted text for this file to the data list
        data.append([project_id, text_1, text_2])

        
# Write the data to the pickle file
with open(output_pickle_path, 'wb') as picklefile:
    pickle.dump(data, picklefile)

# Print a message to indicate the file has been saved
print(f'Data has been saved to {output_pickle_path}.')



# COMMAND ----------

# MAGIC %md
# MAGIC ## 13-17

# COMMAND ----------

"""
Run this part for extracting Preperation and Implementaion in a pickle file from the files from year 2013 to 2017(included)
"""


import re
import os
import pickle

# Specify the folder path containing the .txt files
folder_path = ''

# Specify the custom path for the output pickle file
output_pickle_path = '.pkl'

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

                # Define the start and end patterns
                extracted_text = ""
                text_1 = ""

                start_pattern1 = r"2.1 Project Preparation, Design and Quality at Entry"
                end_pattern1 = r"2.2 Implementation"
                        # Use regular expressions to find the text between the start and end patterns
                start_match = re.search(start_pattern1, text, re.DOTALL | re.IGNORECASE)
                end_match = re.search(end_pattern1, text, re.DOTALL | re.IGNORECASE)

                if start_match and end_match: #and start_match.start() < end_match.start():
                    start_position = start_match.end()  # End position of the start pattern
                    end_position = end_match.start()    # Start position of the end pattern

                    extracted_text = text[start_position:end_position].strip()
                    extracted_text = re.sub(r'\n{3,}', '\n', extracted_text)
                    text_1 = extracted_text
                else:

                    start_pattern1 = r"2.1    Project Preparation, Design and Quality at Entry"
                    end_pattern1 = r"2.2 Implementation"
                            # Use regular expressions to find the text between the start and end patterns
                    start_match = re.search(start_pattern1, text, re.DOTALL | re.IGNORECASE)
                    end_match = re.search(end_pattern1, text, re.DOTALL | re.IGNORECASE)

                    if start_match and end_match: #and start_match.start() < end_match.start():
                        start_position = start_match.end()  # End position of the start pattern
                        end_position = end_match.start()    # Start position of the end pattern

                        extracted_text = text[start_position:end_position].strip()
                        extracted_text = re.sub(r'\n{3,}', '\n', extracted_text)
                        text_1 = extracted_text

                    else:
                        start_pattern1 = r"2.1. Project Preparation, Design, and Quality at Entry"
                        end_pattern1 = r"2.2. Implementation"
                                # Use regular expressions to find the text between the start and end patterns
                        start_match = re.search(start_pattern1, text, re.DOTALL | re.IGNORECASE)
                        end_match = re.search(end_pattern1, text, re.DOTALL | re.IGNORECASE)

                        if start_match and end_match: #and start_match.start() < end_match.start():
                            start_position = start_match.end()  # End position of the start pattern
                            end_position = end_match.start()    # Start position of the end pattern

                            extracted_text = text[start_position:end_position].strip()
                            extracted_text = re.sub(r'\n{3,}', '\n', extracted_text)
                            text_1 = extracted_text

                        else:
                            start_pattern1 = r"2.1 Project Preparation, Design and Quality at Entry|Project Preparation, Design, and Quality at Entry|2.1       Project Preparation, Design and Quality at Entry"
                            end_pattern1 = r"2.2 Implementation|2.2    Implementation|Project Implementation\n\n"
                                    # Use regular expressions to find the text between the start and end patterns
                            start_match = re.search(start_pattern1, text, re.DOTALL | re.IGNORECASE)
                            end_match = re.search(end_pattern1, text, re.DOTALL | re.IGNORECASE)

                            if start_match and end_match: #and start_match.start() < end_match.start():
                                start_position = start_match.end()  # End position of the start pattern
                                end_position = end_match.start()    # Start position of the end pattern

                                extracted_text = text[start_position:end_position].strip()
                                extracted_text = re.sub(r'\n{3,}', '\n', extracted_text)
                                text_1 = extracted_text
                            else:
                                text_1 = "N/A"

                extracted_text = ""
                text_2 = ""

                start_pattern2 = r"2.2. Implementation"
                end_pattern2 = r"2.3. Monitoring and Evaluation \(M&E\) Design, Implementation and Utilization"

                        # Use regular expressions to find the text between the start and end patterns
                start_match = re.search(start_pattern2, text, re.DOTALL | re.IGNORECASE)
                end_match = re.search(end_pattern2, text, re.DOTALL | re.IGNORECASE)

                if start_match and end_match: #and start_match.start() < end_match.start():
                    start_position = start_match.end()  # End position of the start pattern
                    end_position = end_match.start()    # Start position of the end pattern

                    extracted_text = text[start_position:end_position].strip()
                    extracted_text = re.sub(r'\n{3,}', '\n', extracted_text)
                    text_2 = extracted_text


                else:
                    start_pattern2 = r"2.2 Implementation"
                    end_pattern2 = r"2.3 M&E Design, Implementation and Utilization|2.3 Monitoring and Evaluation Design|2.3 Monitoring and Evaluation Design, Implementation, and Utilization"

                            # Use regular expressions to find the text between the start and end patterns
                    start_match = re.search(start_pattern2, text, re.DOTALL | re.IGNORECASE)
                    end_match = re.search(end_pattern2, text, re.DOTALL | re.IGNORECASE)

                    if start_match and end_match: #and start_match.start() < end_match.start():
                        start_position = start_match.end()  # End position of the start pattern
                        end_position = end_match.start()    # Start position of the end pattern

                        extracted_text = text[start_position:end_position].strip()
                        extracted_text = re.sub(r'\n{3,}', '\n', extracted_text)
                        text_2 = extracted_text

                    else:
                        start_pattern2 = r"2.2. Major Factors Affecting Implementation|2.2 Implementation|2.2 Implementation|Project Implementation\n\n|2.2    Implementation|2.2 Major Factors Affecting Implementation"
                        end_pattern2 = r"2.2 Monitoring and Evaluation \(M&E\) Design, Implementation and Utilization|2.3 Monitoring and Evaluation \(M&E\) Design, Implementation, and Utilization|Monitoring and Evaluation\n\n|2.3 Monitoring and Evaluation \(M&E\) Design, Implementation and Utilization|2.3    Monitoring and Evaluation \(M&E\) Design, Implementation and Utilization|2.3 Monitoring and Evaluation \(M&E\) Design, Implementation and Utilization"

                                # Use regular expressions to find the text between the start and end patterns
                        start_match = re.search(start_pattern2, text, re.DOTALL | re.IGNORECASE)
                        end_match = re.search(end_pattern2, text, re.DOTALL | re.IGNORECASE)

                        if start_match and end_match: #and start_match.start() < end_match.start():
                            start_position = start_match.end()  # End position of the start pattern
                            end_position = end_match.start()    # Start position of the end pattern

                            extracted_text = text[start_position:end_position].strip()
                            extracted_text = re.sub(r'\n{3,}', '\n', extracted_text)
                            text_2 = extracted_text
                        else:
                            text_2 = "N/A"
                
                
                

        except FileNotFoundError:
            extracted_texts.append("File not found")

        # Get the project ID for this file
        project_id = extract_project_id_from_file(file_path)
        
        footer_patterns = [
                            r'(?!\d\.)\n+\s+\d{1,2}\s+[A-Z][a-zA-Z]*.*?\(P\d+\)',
                            r'IV. BANK PERFORMANCE, COMPLIANCE ISSUES, AND RISK TO DEVELOPMENT OUTCOME',
                            r'IV\.\s+BANK PERFORMANCE, COMPLIANCE ISSUES, AND RISK TO DEVELOPMENT OUTCOME',
                            r'BANK PERFORMANCE, COMPLIANCE ISSUES, AND RISK TO DEVELOPMENT OUTCOME',
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
        
        text_1 = re.sub(footer_pattern, '', text_1)
        text_1 = re.sub(footer_pattern_again, '', text_1)

        # Append the project ID and extracted text for this file to the data list
        data.append([project_id, text_1, text_2])

        # Append the project ID and extracted text for this file to the data list
        data.append([project_id, text_1, text_2])

        
# Write the data to the pickle file
with open(output_pickle_path, 'wb') as picklefile:
    pickle.dump(data, picklefile)

# Print a message to indicate the file has been saved
print(f'Data has been saved to {output_pickle_path}.')



# COMMAND ----------

"""
Displaying the Result from the output Pickle File
"""

path = output_pickle_path
with open(path, 'rb') as file:
    # Load the contents from the file and store it in a variable
    data = pickle.load(file)


def clean_text(text):
    if isinstance(text, str):
        return text.replace('\xa0', ' ').replace('\n', '\n')
    elif isinstance(text, list):
        return [clean_text(item) for item in text]
    return text

# Process each item in the list
cleaned_data = [clean_text(item) for item in data]

# Now you can use cleaned_data as needed
for item in cleaned_data:
    print(item)