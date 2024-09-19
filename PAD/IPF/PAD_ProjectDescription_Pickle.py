# Databricks notebook source
# MAGIC %md
# MAGIC ## Step 1: Extracting the Project Desciption and Project_ID in a pickle file

# COMMAND ----------

import re
import os
import pickle  # Import the pickle module


# Specify the folder path containing the .txt files
folder_path = ''

# Specify the custom path for the output pickle file
output_path = '.pkl'

# Function to check if "STRATEGIC CONTEXT" exists in the "Table of Contents" page
def check_strategic_context_in_table_of_contents(file_path):
    # Initialize a flag
    found_strategic_context_toc = False

    # Open and read the .txt file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Iterate through each line
    for line in lines:
        # Check if "STRATEGIC CONTEXT" is found in the "Table of Contents" page (case-insensitive)
        if re.search(r'(?i)STRATEGIC CONTEXT', line):
            found_strategic_context_toc = True
            break  # Stop checking once found

    return found_strategic_context_toc

def extract_project_id_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            text = file.read()
            project_id_pattern = r"P\d{6}"
            project_id = re.search(project_id_pattern, text)
            
            if project_id:
                return project_id.group()
            else:
                return "N/A"
    except FileNotFoundError:
        return "File not found"


# Initialize a list to store data for multiple files
data = []

# Iterate over the files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(folder_path, filename)
        exists_in_table_of_contents = check_strategic_context_in_table_of_contents(file_path)

        if exists_in_table_of_contents:
            # Initialize a variable to store the text
            initial_text = ""

            # Initialize a flag to start storing text when "STRATEGIC CONTEXT" is found for the second time
            strategic_context_count = 0

            # Open and read the .txt file
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # Iterate through each line
            for line in lines:
                # Check if "STRATEGIC CONTEXT" is found (case-insensitive)
                if re.search(r'(?i)STRATEGIC CONTEXT', line):
                    strategic_context_count += 1

                    # Start storing text when "STRATEGIC CONTEXT" is found for the second time
                    if strategic_context_count == 2:
                        initial_text += line  # Append the line to the initial_text
                        continue  # Skip further checks for this line

                # Continue storing text after the second occurrence of "STRATEGIC CONTEXT"
                if strategic_context_count >= 2:
                    initial_text += line  # Append the line to the initial_text
        else:
            # Initialize a flag
            found_strategic_context = False

            # Initialize a variable to store the text
            extracted_text = ""

            # Open and read the .txt file
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # Iterate through each line
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

        text = initial_text

        # Define the start and end patterns
        start_pattern = r"(II\..*?PROGRAM DESCRIPTION.*?A\.)|(II\..*?PROJECT DESCRIPTION.*?A\.)|(III\..*?PROGRAM DESCRIPTION.*?A\.)|(III\..*?PROJECT DESCRIPTION.*?A\.)(2\..*?PROGRAM DESCRIPTION.*?A\.)|(2\..*?PROJECT DESCRIPTION.*?A\.)|(3\..*?PROGRAM DESCRIPTION.*?A\.)|(3\..*?PROJECT DESCRIPTION.*?A\.)"
        end_pattern = r"Safeguard and Exception.*?A\.|3\.\s*Implementation.*?A\.|4\.\s*Implementation.*?A\.|III\.\s*IMPLEMENTATION.*?A\.|IV\.\s*IMPLEMENTATION.*?A\.|III\.\s*PROGRAM IMPLEMENTATION.*?A\.|IV\.\s*PROGRAM IMPLEMENTATION.*?A\.|III\.\s*IMPLEMENTATION ARRANGEMENTS.*?A\.|IV\.\s*IMPLEMENTATION ARRANGEMENTS.*?A\.|\.\s*IMPLEMENTATION ARRANGEMENTS.*?A\.|3\.\s*PROGRAM IMPLEMENTATION.*?A\.|4\.\s*PROGRAM IMPLEMENTATION.*?A\.|3\.\s*IMPLEMENTATION ARRANGEMENTS.*?A\.|4\.\s*IMPLEMENTATION ARRANGEMENTS.*?A\."

        # Use regular expressions to find the text between the start and end patterns
        start_match = re.search(start_pattern, text, re.DOTALL | re.IGNORECASE)
        end_match = re.search(end_pattern, text, re.DOTALL | re.IGNORECASE)

        if start_match and end_match:
            start_position = start_match.end()  # End position of the start pattern
            end_position = end_match.start()    # Start position of the end pattern

            extracted_text = text[start_position:end_position].strip()
            final_text = extracted_text

        # Append data for this file to the list
        data.append([extract_project_id_from_file(file_path), final_text])



# Save the data list to a pickle file
with open(output_path, 'wb') as pickle_file:
    pickle.dump(data, pickle_file)

# Print a message to indicate the file has been saved
print(f'Data saved to {output_path}')



# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 2: Displaying the data from the saved pickle file

# COMMAND ----------

# Load the data from the pickle file
with open(output_path, 'rb') as pickle_file:
    data = pickle.load(pickle_file)

# Accessing the data as a list of lists
# Iterating through the data and printing it
for item in data:
    project_id, text = item
    print(f'Project ID: {project_id}\n')
    print(f'PROJECT DESCRIPTION:\n\n {text}')
    print('\n')



# COMMAND ----------

