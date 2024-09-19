# Databricks notebook source
# MAGIC %md
# MAGIC ## a. Run this part if the PAD files are from year 2019 and onwards

# COMMAND ----------

import re
import os
import csv # Import the pickle module


# Specify the folder path containing the .txt files
folder_path = ''

# Specify the custom path for the output pickle file. Make sure its in ".csv" format
output_path = '.csv'
output_pickle_path = '.pkl'

def check_strategic_context_in_table_of_contents(file_path):
    # List of encodings to try
    encodings = ['utf-8', 'latin-1', 'utf-16', 'iso-8859-1', 'cp1252']

    for encoding in encodings:
        try:
            # Attempt to open and read the .txt file with the current encoding
            with open(file_path, 'r', encoding=encoding) as file:
                lines = file.readlines()

            # Iterate through each line
            for line in lines:
                # Check if "STRATEGIC CONTEXT" is found in the "Table of Contents" page (case-insensitive)
                if re.search(r'(?i)STRATEGIC CONTEXT', line):
                    return True  # Return True if found
            return False  # Return False if not found in any encoding

        except UnicodeDecodeError:
            continue  # If decoding fails with the current encoding, try the next one

    return False  # Return False if not found with any encoding



    
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

def extract_non_WBG_financing(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            text = file.read()
            extracted_text = ""
            text_6 = ""
            start_pattern6 = r"Non-World Bank Group Financing"
            end_pattern6 = r"Expected Disbursements|IDA Resources"

            # Use regular expressions to find the tother oext between the start and end patterns
            start_match = re.search(start_pattern6, text, re.DOTALL | re.IGNORECASE)
            end_match = re.search(end_pattern6, text, re.DOTALL | re.IGNORECASE)

            if start_match and end_match:
                start_position = start_match.end()  # End position of the start pattern
                end_position = end_match.start()    # Start position of the end pattern

                extracted_text = text[start_position:end_position].strip()

                if extracted_text:
                    # Define a pattern to capture the footer notes
                    footer_patterns = [
                        r'Page \d+ of \d+',
                        r'Page \d+',
                        r'The World Bank\s+(.*?)\s+\(P\d+\)',  
                        r'(\d+)\s+of\s+(\d+)'
                    ]

                    footer_pattern = re.compile('|'.join(footer_patterns), re.DOTALL)

                    # Remove footer notes
                    extracted_text = re.sub(footer_pattern, '', extracted_text)

                    text_6 = extracted_text
                else:
                    text_6 = "N/A"

        return text_6
            
    except FileNotFoundError:
        return "File not found"


# Initialize a list to store data for multiple files
data = []

# Iterate over the files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(folder_path, filename)
        exists_in_table_of_contents = check_strategic_context_in_table_of_contents(file_path)
        
        initial_text = ""
        if exists_in_table_of_contents:
            # Initialize a variable to store the text
            #initial_text = ""
            strategic_context_count = 0

            # Open and read the .txt file, specifying the encoding
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                lines = file.readlines()

            for line in lines:
                # Check if "STRATEGIC CONTEXT" is found (case-insensitive)
                if re.search(r'(?i)STRATEGIC CONTEXT', line):
                    strategic_context_count += 1

                    # Start storing text when "STRATEGIC CONTEXT" is found for the second time
                    if strategic_context_count == 2:
                        initial_text += line
                elif strategic_context_count >= 2:
                    initial_text += line

        else:
            # Initialize a flag
            found_strategic_context = False

            # Initialize a variable to store the text
            extracted_text = ""
            

            # Open and read the .txt file, specifying the encoding
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                lines = file.readlines()

            for line in lines:
                # Check if "STRATEGIC CONTEXT" is found (case-insensitive)
                if re.search(r'(?i)STRATEGIC CONTEXT', line):
                    if not found_strategic_context:
                        found_strategic_context = True
                    else:
                        # Start storing text after the first occurrence of "STRATEGIC CONTEXT"
                        extracted_text += line
                elif found_strategic_context:
                    # Continue storing text after the first occurrence of "STRATEGIC CONTEXT"
                    extracted_text += line
                    initial_text = extracted_text
    

        # Call the function to remove lines with page numbers from the content
        #text = remove_page_numbers(initial_text)
        text = initial_text
        
        final_text = ""
        # Define the start and end patterns
        start_pattern = r"PDO Level Indicators|C\.\s+PDO-Level|C\.\s+PDO-LEVEL RESULTS INDICATORS"
        end_pattern = r"B\. Project Components|\s+ PROJECT DESCRIPTION|III\.\sPROJECT DESCRIPTION"
        # Use regular expressions to find the text between the start and end patterns
        start_match = re.search(start_pattern, text, re.DOTALL | re.IGNORECASE)
        end_match = re.search(end_pattern, text, re.DOTALL | re.IGNORECASE)

        if start_match and end_match:
            start_position = start_match.end()  # End position of the start pattern
            end_position = end_match.start()    # Start position of the end pattern

            extracted_text = text[start_position:end_position].strip()

            if extracted_text:
                # Define a pattern to capture the footer notes
                footer_patterns = [
                    r'(?!\d\.)\n+\s+\d{1,2}\s+[A-Z][a-zA-Z]*.*?\(P\d+\)',
                    r'(?!\d\.)\n+\s+\d{1,2}[A-Z][a-zA-Z]*.*?\(P\d+\)',
                    r'(?!\d\.)\n\d{1,2}\s+[A-Z][a-zA-Z]*.*?\(P\d+\)',
                    r'(?!\d\.)\n+\d{1,2}\s+[A-Z][a-zA-Z]*.*?\(P\d+\)',
                    r'(?!\d\.)\n+\d{1,2}\s+[A-Z][a-zA-Z]*.*?\(P\d+\)',
                    r'(?!\d\.)\n\d{1,2}[A-Z][a-zA-Z]*.*?\(P\d+\)',
                    r'(?!\d\.)\n+\d{1,2}[A-Z][a-zA-Z]*.*?\(P\d+\)',
                    r'Page \d+ of \d+',
                    r'Page \d+',
                    r'The World Bank\s+(.*?)\s+\(P\d+\)',   
                    r'(\d+)\s+of\s+(\d+)'
                ]

                footer_pattern = re.compile('|'.join(footer_patterns), re.DOTALL)

                # Remove footer notes
                extracted_text = re.sub(footer_pattern, '', extracted_text)

                final_text = extracted_text
            else:
                final_text = "N/A"
            
        # Define the start and end patterns
        extracted_text = ""
        text_2 = ""
        start_pattern2 = r"C\.\s*Project Beneficiaries|C. Project Beneficiaries|D. Project Beneficiaries|B. Project Beneficiaries|B\.\s+PROJECT BENEFICIARIES"
        end_pattern2 = r"C. PDO-Level Results Indicators|D. Project Financing|C\.\s+PDO-LEVEL|D. Rationale for Bank Involvement and Role of Partners|[A-Z]\.Theory of Change|[A-Z]\.Results Chain|[A-Z]\.\s*Theory of Change|[A-Z]\.\s*Results Chain"
        # Use regular expressions to find the text between the start and end patterns
        start_match = re.search(start_pattern2, text, re.DOTALL | re.IGNORECASE)
        end_match = re.search(end_pattern2, text, re.DOTALL | re.IGNORECASE)

        if start_match and end_match:
            start_position = start_match.end()  # End position of the start pattern
            end_position = end_match.start()    # Start position of the end pattern

            extracted_text = text[start_position:end_position].strip()

            if extracted_text:
                # Define a pattern to capture the footer notes
                footer_patterns = [
                    r'(?!\d\.)\n+\s+\d{1,2}\s+[A-Z][a-zA-Z]*.*?\(P\d+\)',
                    r'(?!\d\.)\n+\s+\d{1,2}[A-Z][a-zA-Z]*.*?\(P\d+\)',
                    r'(?!\d\.)\n\d{1,2}\s+[A-Z][a-zA-Z]*.*?\(P\d+\)',
                    r'(?!\d\.)\n+\d{1,2}\s+[A-Z][a-zA-Z]*.*?\(P\d+\)',
                    r'(?!\d\.)\n+\d{1,2}\s+[A-Z][a-zA-Z]*.*?\(P\d+\)',
                    r'(?!\d\.)\n\d{1,2}[A-Z][a-zA-Z]*.*?\(P\d+\)',
                    r'(?!\d\.)\n+\d{1,2}[A-Z][a-zA-Z]*.*?\(P\d+\)',
                    r'Page \d+ of \d+',
                    r'Page \d+',
                    r'The World Bank\s+(.*?)\s+\(P\d+\)', 
                    r'(\d+)\s+of\s+(\d+)'
                ]

                footer_pattern = re.compile('|'.join(footer_patterns), re.DOTALL)

                # Remove footer notes
                extracted_text = re.sub(footer_pattern, '', extracted_text)

                text_2 = extracted_text
            else:
                text_2 = "N/A"
        
        # Define the start and end patterns
        extracted_text = ""
        text_3 = ""
        start_pattern3 = r"ROLE OF OTHER PARTNERS IN THE AREAS OF PRIVATE SECTOR COMPETITIVENESS|D. Role of Partners|F. Rationale for Bank Involvement and Role of Partners|\nE\. Rationale for Bank Involvement and Role of partners|E. Rationale for World Bank Involvement and Role of Partners|E. Rationale for Bank Involvement and Role of Partners\n|D\. Rationale for Bank Involvement and Role of partners|D. Rationale for Bank Involvement and Role of Partners"
        end_pattern3 = r"ANNEX 9:|V. KEY RISKS|G. Lessons Learned and Reflected in the Project Design|F. Lessons Learned and Reflected in the Project Design|F\. Lessons Learned and Reflected in the Project Design|E\. Lessons Learned and Reflected in the Project Design|E. Lessons Learned and Progress on Learning Agenda|F. Lessons Learned and Progress on Learning Agenda"
        # Use regular expressions to find the text between the start and end patterns
        start_match = re.search(start_pattern3, text, re.DOTALL | re.IGNORECASE)
        end_match = re.search(end_pattern3, text, re.DOTALL | re.IGNORECASE)

        if start_match and end_match:
            start_position = start_match.end()  # End position of the start pattern
            end_position = end_match.start()    # Start position of the end pattern

            extracted_text = text[start_position:end_position].strip()

            if extracted_text:
                # Define a pattern to capture the footer notes
                footer_patterns = [
                    r'(?!\d\.)\n+\s+\d{1,2}\s+[A-Z][a-zA-Z]*.*?\(P\d+\)',
                    r'(?!\d\.)\n+\s+\d{1,2}[A-Z][a-zA-Z]*.*?\(P\d+\)',
                    r'(?!\d\.)\n\d{1,2}\s+[A-Z][a-zA-Z]*.*?\(P\d+\)',
                    r'(?!\d\.)\n+\d{1,2}\s+[A-Z][a-zA-Z]*.*?\(P\d+\)',
                    r'(?!\d\.)\n+\d{1,2}\s+[A-Z][a-zA-Z]*.*?\(P\d+\)',
                    r'(?!\d\.)\n\d{1,2}[A-Z][a-zA-Z]*.*?\(P\d+\)',
                    r'(?!\d\.)\n+\d{1,2}[A-Z][a-zA-Z]*.*?\(P\d+\)',
                    r'Page \d+ of \d+',
                    r'Page \d+',
                    r'The World Bank\s+(.*?)\s+\(P\d+\)',  
                    r'(\d+)\s+of\s+(\d+)'
                ]

                footer_pattern = re.compile('|'.join(footer_patterns), re.DOTALL)

                # Remove footer notes
                extracted_text = re.sub(footer_pattern, '', extracted_text)

                text_3 = extracted_text
            else:
                text_3 = "N/A"
        
        # Define the start and end patterns
        extracted_text = ""
        text_4 = ""
        start_pattern4 = r"Lessons Learned and Reflected in the Project Design|E. Lessons Learned and Progress on Learning Agenda|F. Lessons Learned and Progress on Learning Agenda"
        end_pattern4 = r"Project Components*?A\.|B\.\s*Project Components*?A\.|4\.\s*Implementation.*?A\.|III\.\s*IMPLEMENTATION.*?A\.|IV\.\s*IMPLEMENTATION.*?A\.|III\.\s*PROGRAM IMPLEMENTATION.*?A\.|IV\.\s*PROGRAM IMPLEMENTATION.*?A\.|III\.\s*IMPLEMENTATION ARRANGEMENTS.*?A\.|IV\.\s*IMPLEMENTATION ARRANGEMENTS.*?A\.|\.\s*IMPLEMENTATION ARRANGEMENTS.*?A\.|3\.\s*PROGRAM IMPLEMENTATION.*?A\.|4\.\s*PROGRAM IMPLEMENTATION.*?A\.|3\.\s*IMPLEMENTATION ARRANGEMENTS.*?A\.|4\.\s*IMPLEMENTATION ARRANGEMENTS.*?A\."
        # Use regular expressions to find the text between the start and end patterns
        start_match = re.search(start_pattern4, text, re.DOTALL | re.IGNORECASE)
        end_match = re.search(end_pattern4, text, re.DOTALL | re.IGNORECASE)

        if start_match and end_match:
            start_position = start_match.end()  # End position of the start pattern
            end_position = end_match.start()    # Start position of the end pattern

            extracted_text = text[start_position:end_position].strip()

            if extracted_text:
                # Define a pattern to capture the footer notes
                footer_patterns = [
                    r'(?!\d\.)\n+\s+\d{1,2}\s+[A-Z][a-zA-Z]*.*?\(P\d+\)',
                    r'(?!\d\.)\n+\s+\d{1,2}[A-Z][a-zA-Z]*.*?\(P\d+\)',
                    r'(?!\d\.)\n\d{1,2}\s+[A-Z][a-zA-Z]*.*?\(P\d+\)',
                    r'(?!\d\.)\n+\d{1,2}\s+[A-Z][a-zA-Z]*.*?\(P\d+\)',
                    r'(?!\d\.)\n+\d{1,2}\s+[A-Z][a-zA-Z]*.*?\(P\d+\)',
                    r'(?!\d\.)\n\d{1,2}[A-Z][a-zA-Z]*.*?\(P\d+\)',
                    r'(?!\d\.)\n+\d{1,2}[A-Z][a-zA-Z]*.*?\(P\d+\)',
                    r'Page \d+ of \d+',
                    r'Page \d+',
                    r'The World Bank\s+(.*?)\s+\(P\d+\)', 
                    r'(\d+)\s+of\s+(\d+)'
                ]

                footer_pattern = re.compile('|'.join(footer_patterns), re.DOTALL)

                # Remove footer notes
                extracted_text = re.sub(footer_pattern, '', extracted_text)

                text_4 = extracted_text
            else:
                text_4 = "N/A"
        
        # Define the start and end patterns
        extracted_text = ""
        text22 = initial_text
        text_5 = ""
        start_pattern5 = r"RESULTS FRAMEWORK AND MONITORING|RESULTS FRAMEWORK /AND MONITORING|\s{2,}RESULTS FRAMEWORK\s{2,}"
        end_pattern5 = r"ANNEX 1:"
        # Use regular expressions to find the tother oext between the start and end patterns
        start_match = re.search(start_pattern5, text22, re.DOTALL | re.IGNORECASE)
        end_match = re.search(end_pattern5, text22, re.DOTALL | re.IGNORECASE)

        if start_match and end_match:
            start_position = start_match.end()  # End position of the start pattern
            end_position = end_match.start()    # Start position of the end pattern

            extracted_text = text[start_position:end_position].strip()

            if extracted_text:
                # Define a pattern to capture the footer notes
                footer_patterns = [
                    r'Page \d+ of \d+',
                    r'Page \d+',
                    r'The World Bank\s+(.*?)\s+\(P\d+\)',  
                    r'(\d+)\s+of\s+(\d+)'
                ]

                footer_pattern = re.compile('|'.join(footer_patterns), re.DOTALL)

                # Remove footer notes
                extracted_text = re.sub(footer_pattern, '', extracted_text)

                text_5 = extracted_text
            else:
                text_5 = "N/A"
            
        

        # Append data for this file to the list
        data.append([extract_project_id_from_file(file_path),extract_non_WBG_financing(file_path), final_text, text_2, text_3, text_4, text_5])


# Write the data to the CSV file
with open(output_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Project ID','Non-WBG Financing (US$, Millions)', 'PDO Level Indicator', 'Project Beneficiaries', 'Role of partners','Lessons Learned and Reflected in the Project Design','RESULTS FRAMEWORK AND MONITORING'])
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
# MAGIC ## b. Run this part if the files are from before year 2019

# COMMAND ----------

import re
import os
import csv  # Import the csv module


# Specify the folder path containing the .txt files
folder_path = ''

# Specify the custom path for the output pickle file. Make sure its in ".csv" format
output_path = '.csv'

output_pickle_path = '.pkl'


def check_strategic_context_in_table_of_contents(file_path):
    # List of encodings to try
    encodings = ['utf-8', 'latin-1', 'utf-16', 'iso-8859-1', 'cp1252']

    for encoding in encodings:
        try:
            # Attempt to open and read the .txt file with the current encoding
            with open(file_path, 'r', encoding=encoding) as file:
                lines = file.readlines()

            # Iterate through each line
            for line in lines:
                # Check if "STRATEGIC CONTEXT" is found in the "Table of Contents" page (case-insensitive)
                if re.search(r'(?i)STRATEGIC CONTEXT', line):
                    return True  # Return True if found
            return False  # Return False if not found in any encoding

        except UnicodeDecodeError:
            continue  # If decoding fails with the current encoding, try the next one

    return False  # Return False if not found with any encoding

# Define a function to remove lines with page numbers from a text string
def remove_page_numbers(content_bad):
    pattern = r'^\d+$|Page \d+ of \d+'
    pattern2 = r'Page \d+'

    # Use re.MULTILINE to apply the pattern to each line in the text
    modified_text = re.sub(pattern, '', content_bad, flags=re.MULTILINE)
    
    modified_text_final = re.sub(pattern2, '', modified_text, flags=re.MULTILINE)

    return modified_text_final

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

def extract_non_WBG_financing(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            text = file.read()
            extracted_text = ""
            text_6 = ""
            start_pattern6 = r"Non-World Bank Group Financing"
            end_pattern6 = r"Expected Disbursements|IDA Resources"

            # Use regular expressions to find the tother oext between the start and end patterns
            start_match = re.search(start_pattern6, text, re.DOTALL | re.IGNORECASE)
            end_match = re.search(end_pattern6, text, re.DOTALL | re.IGNORECASE)

            if start_match and end_match:
                start_position = start_match.end()  # End position of the start pattern
                end_position = end_match.start()    # Start position of the end pattern

                extracted_text = text[start_position:end_position].strip()
                text_6 = extracted_text
            else:
                text_6 = "N/A"

        return text_6
            
    except FileNotFoundError:
        return "File not found"


# Initialize a list to store data for multiple files
data = []

# Iterate over the files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(folder_path, filename)
        exists_in_table_of_contents = check_strategic_context_in_table_of_contents(file_path)
        
        initial_text = ""
        if exists_in_table_of_contents:
            # Initialize a variable to store the text
            #initial_text = ""
            strategic_context_count = 0

            # Open and read the .txt file, specifying the encoding
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                lines = file.readlines()

            for line in lines:
                # Check if "STRATEGIC CONTEXT" is found (case-insensitive)
                if re.search(r'(?i)STRATEGIC CONTEXT', line):
                    strategic_context_count += 1

                    # Start storing text when "STRATEGIC CONTEXT" is found for the second time
                    if strategic_context_count == 2:
                        initial_text += line
                elif strategic_context_count >= 2:
                    initial_text += line

        else:
            # Initialize a flag
            found_strategic_context = False

            # Initialize a variable to store the text
            extracted_text = ""
            

            # Open and read the .txt file, specifying the encoding
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                lines = file.readlines()

            for line in lines:
                # Check if "STRATEGIC CONTEXT" is found (case-insensitive)
                if re.search(r'(?i)STRATEGIC CONTEXT', line):
                    if not found_strategic_context:
                        found_strategic_context = True
                    else:
                        # Start storing text after the first occurrence of "STRATEGIC CONTEXT"
                        extracted_text += line
                elif found_strategic_context:
                    # Continue storing text after the first occurrence of "STRATEGIC CONTEXT"
                    extracted_text += line
                    initial_text = extracted_text
        
        # Call the function to remove lines with page numbers from the content
        text = remove_page_numbers(initial_text)
        final_text = ""
        # Define the start and end patterns
        start_pattern = r"PDO Level Results Indicators|PDO Level Indicators|C\.\s+PDO-Level|C\.\s+PDO-LEVEL RESULTS INDICATORS|PDO Level Results Indicators"
        end_pattern = r"B\. Project Components|\s+ PROJECT DESCRIPTION|III\.\sPROJECT DESCRIPTION"
        # Use regular expressions to find the text between the start and end patterns
        start_match = re.search(start_pattern, text, re.DOTALL | re.IGNORECASE)
        end_match = re.search(end_pattern, text, re.DOTALL | re.IGNORECASE)

        if start_match and end_match:
            start_position = start_match.end()  # End position of the start pattern
            end_position = end_match.start()    # Start position of the end pattern

            extracted_text = text[start_position:end_position].strip()
            #final_text = extracted_text
            if extracted_text:
                final_text = extracted_text
            else:
                final_text = "N/A"
            
        # Define the start and end patterns
        extracted_text = ""
        text_2 = ""
        start_pattern2 = r"Project Beneficiaries|C\.\s*Project Beneficiaries|C. Project Beneficiaries|D. Project Beneficiaries|D\.\s+Project Beneficiaries|B. Project Beneficiaries|B\.\s+PROJECT BENEFICIARIES|B\.\s+Project Beneficiaries"
        end_pattern2 = r"PDO Level Results Indicators|C. PDO-Level Results Indicators|B. Key Results Indicators|C\.\s+PDO-LEVEL|D. Rationale for Bank Involvement and Role of Partners|[A-Z]\.Theory of Change|[A-Z]\.Results Chain|[A-Z]\.\s*Theory of Change|[A-Z]\.\s*Results Chain"
        # Use regular expressions to find the text between the start and end patterns
        start_match = re.search(start_pattern2, text, re.DOTALL | re.IGNORECASE)
        end_match = re.search(end_pattern2, text, re.DOTALL | re.IGNORECASE)

        if start_match and end_match:
            start_position = start_match.end()  # End position of the start pattern
            end_position = end_match.start()    # Start position of the end pattern

            extracted_text = text[start_position:end_position].strip()
            #text_2 = extracted_text
            if extracted_text:
                text_2 = extracted_text
            else:
                text_2 = "N/A"
        
        # Define the start and end patterns
        extracted_text = ""
        text_3 = ""
        start_pattern3 = r"ROLE OF OTHER PARTNERS IN THE AREAS OF PRIVATE SECTOR COMPETITIVENESS|D. Role of Partners|F. Rationale for Bank Involvement and Role of Partners|Role of Partners\s+|\nE\. Rationale for Bank Involvement and Role of partners|E. Rationale for World Bank Involvement and Role of Partners|E. Rationale for Bank Involvement and Role of Partners\n|D\. Rationale for Bank Involvement and Role of partners|D. Rationale for Bank Involvement and Role of Partners"
        end_pattern3 = r"ANNEX 4:|ANNEX 9:|V. KEY RISKS|G. Lessons Learned and Reflected in the Project Design|F. Lessons Learned and Reflected in the Project Design|F\. Lessons Learned and Reflected in the Project Design|E\. Lessons Learned and Reflected in the Project Design|E. Lessons Learned and Progress on Learning Agenda|F. Lessons Learned and Progress on Learning Agenda"
        # Use regular expressions to find the text between the start and end patterns
        start_match = re.search(start_pattern3, text, re.DOTALL | re.IGNORECASE)
        end_match = re.search(end_pattern3, text, re.DOTALL | re.IGNORECASE)

        if start_match and end_match:
            start_position = start_match.end()  # End position of the start pattern
            end_position = end_match.start()    # Start position of the end pattern

            extracted_text = text[start_position:end_position].strip()
            #text_3 = extracted_text
            if extracted_text:
                text_3 = extracted_text
            else:
                text_3 = "N/A"
        
        # Define the start and end patterns
        extracted_text = ""
        text_4 = ""
        start_pattern4 = r"C. Lessons Learned Reflected in the Project Design|Lessons Learned and Reflected in the Project Design|E. Lessons Learned and Progress on Learning Agenda|F. Lessons Learned and Progress on Learning Agenda"
        end_pattern4 = r"Project Components*?A\.|B\.\s*Project Components*?A\.|4\.\s*Implementation.*?A\.|III\.\s*IMPLEMENTATION.*?A\.|IV\.\s*IMPLEMENTATION.*?A\.|III\.\s*PROGRAM IMPLEMENTATION.*?A\.|IV\.\s*PROGRAM IMPLEMENTATION.*?A\.|III\.\s*IMPLEMENTATION ARRANGEMENTS.*?A\.|IV\.\s*IMPLEMENTATION ARRANGEMENTS.*?A\.|\.\s*IMPLEMENTATION ARRANGEMENTS.*?A\.|3\.\s*PROGRAM IMPLEMENTATION.*?A\.|4\.\s*PROGRAM IMPLEMENTATION.*?A\.|3\.\s*IMPLEMENTATION ARRANGEMENTS.*?A\.|4\.\s*IMPLEMENTATION ARRANGEMENTS.*?A\."
        # Use regular expressions to find the text between the start and end patterns
        start_match = re.search(start_pattern4, text, re.DOTALL | re.IGNORECASE)
        end_match = re.search(end_pattern4, text, re.DOTALL | re.IGNORECASE)

        if start_match and end_match:
            start_position = start_match.end()  # End position of the start pattern
            end_position = end_match.start()    # Start position of the end pattern

            extracted_text = text[start_position:end_position].strip()
            #text_4 = extracted_text
            if extracted_text:
                text_4 = extracted_text
            else:
                text_4 = "N/A"
        
        # Define the start patterns for both codes
       # Define the combined start and end patterns
        start_pattern = r"\s+ VII\. RESULTS FRAMEWORK AND MONITORING|RESULTS FRAMEWORK /AND MONITORING|Annex 1: Results Framework and Monitoring|\n\s+ANNEX 1: RESULTS FRAMEWORK AND MONITORING|\s+ VII\. RESULTS FRAMEWORK AND MONITORING"
        end_pattern = r"ANNEX 1:|ANNEX 2:"

        # Use a try-except block to handle regex errors
        try:
            # Use regular expressions to find the text between the start pattern and the end pattern
            start_match = re.search(start_pattern, text, re.DOTALL | re.IGNORECASE)

            if start_match:
                start_position = start_match.end()  # End position of the start pattern

                # Check if there is an end pattern
                end_match = re.search(end_pattern, text[start_position:], re.DOTALL | re.IGNORECASE)

                if end_match:
                    end_position = end_match.start() + start_position  # Start position of the end pattern
                else:
                    # If no end pattern is found, set end_position to the end of the file
                    end_position = len(text)

                extracted_text = text[start_position:end_position].strip()
                text_5 = extracted_text
            else:
                text_5 = "N/A"
        except re.error:
            text_5 = "Regex error: Your regular expression is not valid"

      

        # Append data for this file to the list
        data.append([extract_project_id_from_file(file_path),extract_non_WBG_financing(file_path), final_text, text_2, text_3, text_4, text_5])

# Write the data to the CSV file
with open(output_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Project ID','Non-WBG Financing (US$, Millions)', 'PDO Level Indicator', 'Project Beneficiaries', 'Role of partners','Lessons Learned and Reflected in the Project Design','RESULTS FRAMEWORK AND MONITORING'])
    csvwriter.writerows(data)

# Write the data to the pickle file
with open(output_pickle_path, 'wb') as picklefile:
    pickle.dump(data, picklefile)

# Print a message to indicate the file has been saved
print(f'Data has been saved to {output_pickle_path}.')

# Print a message to indicate the file has been saved
print(f'Data has been saved to {output_path}')





# COMMAND ----------

