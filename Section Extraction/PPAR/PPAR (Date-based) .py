# Databricks notebook source
# MAGIC %md
# MAGIC #### ***Step One: Load the environment***

# COMMAND ----------

import os, re, sys  # Importing the os and re modules
import time  # Importing the time module
import pandas as pd  # Importing the pandas library
from APIDocInfo import DocInfoGen  # Importing the DocInfoGen class from the APIDocInfo module
from bulkDownload import bulk_download_date  # Importing the bulk_download_date function from the script_updated module

# COMMAND ----------

# MAGIC %md
# MAGIC #### ***Step two: Function definition***

# COMMAND ----------

def bulk_download_files(data_folder, file_type, download_version, start_date, end_date, file_number):
    """
    Bulk download files based on specified parameters.

    Args:
        data_folder (str): Path to the data folder where the files will be saved.
        file_type (str or list): File type(s) to download.
        download_version (str): Download version ('txt' or 'pdf').
        start_date (str): Start date for downloading files.
        end_date (str): End date for downloading files.
        file_number (int): Number of files to download.

    Returns:
        None
    """
    # Create a dictionary with the specified parameters
    input_dict = {
        'root_path': data_folder,
        'document_type': file_type,
        'file_number': file_number,
        'start_date': start_date,
        'end_date': end_date,
        'download_version': download_version
    }
    # Call the function to perform bulk file download with the input dictionary
    bulk_download_date(input_dict)

def clean_text(text):
    """
    Clean the text by removing multiple spaces and leading/trailing spaces.

    Args:
        text (str): The text to be cleaned.

    Returns:
        str: The cleaned text.
    """
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = text.strip()  # Remove leading and trailing spaces
    return text

def process_ppar_lessons(data_folder):
    """
    Process PPAR lessons from files in the specified data folder.

    Args:
        data_folder (str): Path to the data folder containing the PPAR files.

    Returns:
        pandas.DataFrame: DataFrame containing the extracted PPAR lessons and project IDs.
    """   
    # Check if the download folder is empty
    if not os.listdir(f"{data_folder}/ppar_folder"):
        error_message = "The download folder is empty. Please recheck the download section. Aborting the execution."
        print(error_message)
    ppar_lessons_patterns_list = [
        # patterns to identify lessons in the files
        r'(\n+\s*lessons\n+.*?)3. Poverty Reduction Support Credit 8-9',
        r'(\n+\d\.\s+lessons\n+.*?)(?:(?:References)|(?:ANNEX A)|(?:Appendix A)|(?:Epilogue)|(?:Bibliography))',
        r"(\n+lessons\n+\d\.(?:\d{1,3})?.*?)(?:(?:Bibliography)|(?:ANNEX A)|(?:Appendix A)|(?:References)|(?:Epilogue))",
        r"\n+(?:\x0c)?(?:\s+)?(\d+\s*\.?\s+(?:common\s)?(?:(?:(?:findings?)|(?:discussions?)|(?:themes?)|(?:looking forward)|(?:conclusions?))\s?and\s?)?lessons.*?\n+(?:\s+)?(?:\x0c)*)(?:\d\s*\.?\s+)?(?:(?:bibliography)|(?:REFERENCES)|(?:ANNEX A)|(?:Appendix A)|(?:Epilogue))",
        r"\n+Lessons\n+.*?\n\x0c(?:(?:Bibliography)|(?:ANNEX A)|(?:Appendix A)|(?:Epilogue))",
        r"\n+((?:\x0c)?(?:\s+)?lessons\n+(?:\s+)?\d+.*?\n(?:\x0c)+)(?:(?:bibliography)|(?:REFERENCES)|(?:ANNEX A)|(?:Appendix A)|(?:Epilogue))",
        r"\n+((?:\x0c)?(?:\s+)?lessons\n+(?:\s+)?The following lessons.*?\n(?:\x0c)+)(?:(?:bibliography)|(?:REFERENCES)|(?:ANNEX A)|(?:Appendix A)|(?:Epilogue))",
        r"(\n+(?:\s+)?lessons\n+\d+\..*?\n+(?:(?:\x0c)+)?)(?:(?:bibliography)|(?:REFERENCES)|(?:ANNEX A)|(?:Appendix A)|(?:Epilogue))",
        r"(\n{6}lessons\n{2}.*?\n+(?:(?:\x0c)+)?)(?:(?:bibliography)|(?:REFERENCES)|(?:ANNEX A)|(?:Appendix A)|(?:Epilogue))",
        r"\n+(?:\x0c)?(?:\s+)?(\d+\.?\s+(?:common\s)?lessons.*?\n+(?:\x0c){0,})Appendix",
        r"(\n{4}lessons\n{2}\s+Two main lessons.*?\n+(?:(?:\x0c)+)?)(?:(?:bibliography)|(?:REFERENCES)|(?:ANNEX A)|(?:Appendix A)|(?:Epilogue))",
        r"\n+(common experiences and potential lessons\n+\d+\.?(?:\d)?.*?)\n+(?:(?:references)|(?:ANNEX A)|(?:Appendix A)|(?:Epilogue)|(?:Bibliography))",
        r"\n+(?:\x0c)?(?:\s+)?(\d+\.?\s+(?:common\s)?(?:(?:(?:discussions?)|(?:findings?)|(?:themes?)|(?:looking forward)|(?:conclusions?))\s?and\s?)?lessons.*?\n+(?:\s+)?(?:\x0c){0,})(?:\d\.?\s+)?Annex(?:A|1|(?:\s1)|(?:\sA)|(?:\sI))",
        r"(\n+(?:\s+)?lessons\n+\d+\..*?\n+(?:(?:\x0c)+)?)Annex(?:A|1|(?:\s1)|(?:\sA)|(?:\sI))",
        r"\n+(?:\s+)?lessons derived from the three projects.*?",
        r"\n+(?:\x0c)?(?:\s+)?((?:common\s)?(?:(?:(?:findings?)|(?:discussions?)|(?:themes?)|(?:looking forward)|(?:conclusions?))\s?and\s)?lessons.*?\n+(?:\s+)?(?:\x0c){0,})(?:\d\.?\s+)?Annex(?:A|1|(?:\s1)|(?:\sA)|(?:\sI))",
        r'(\n+\d\s*\.\s+Lessons\n.*?)\n+(?:(?:Bibliography)|(?:References)|(?:ANNEX A)|(?:Appendix A)|(?:Epilogue))',
        r'(\n+Lessons derived from the three projects.*?)Vinod Thomas',
    ]
    ppar_list = os.listdir(f"{data_folder}/ppar_folder")  # Get the list of files in the ppar_folder
    ppar_list = [p for p in ppar_list if not p.startswith('.')]  # Exclude files starting with '.'
    lessons_df = []  # Initialize an empty list to store the PPAR lessons
    cut_index = 4  # Initialize the cut index
    for ppar_file in ppar_list:  # Iterate through each PPAR file
        full_path = os.path.join(data_folder, 'ppar_folder', ppar_file)  # Get the full path of the file
        with open(full_path, 'r', errors='ignore') as f:  # Open the file in read mode, ignoring errors
            pid_list = re.findall(r'P\d+', f.read())  # Find all occurrences of 'P' followed by digits in the file content
            if not pid_list:
                continue  # Skip the iteration if no match is found
            pid = pid_list[0]  # Get the first matching project ID
            f.seek(0)  # Reset the file pointer to the beginning
            text = f.read()  # Read the file content

            if ppar_file.startswith('2018'):  # Check if the file name starts with '2018'. Before 2018 format was different. 
                cut_index = 4  # Set the cut index to 4
            cut = int(len(text) / cut_index)  # Calculate the cut position based on the cut index
            text = text[cut:]  # Remove the content before the cut position
            text = re.sub(r'\ufeff', '', text)  # Remove the Unicode BOM character
            for form in ppar_lessons_patterns_list:  # Iterate through each pattern in the list
                lesson = re.findall(form, text, flags=re.I | re.S)  # Find all occurrences of the pattern in the text
                if len(lesson) > 0:  # If at least one match is found
                    tmp_dict = {}  # Create a temporary dictionary to store the project ID and PPAR lessons
                    tmp_dict['Project ID'] = pid  # Store the project ID
                    tmp_dict['PPAR Lessons'] = clean_text(lesson[0])  # Store the cleaned PPAR lesson text
                    lessons_df.append(tmp_dict)  # Append the temporary dictionary to the lessons_df list
                    break  # Break the loop, as we have found a match for the PPAR lessons
    lessons_df = pd.DataFrame(lessons_df)  # Create a DataFrame from the lessons_df list
    return lessons_df

def process_ppar_info(data_folder):
    """
    Process PPAR information and save it to an Excel file.

    Args:
        data_folder (str): Path to the data folder containing the PPAR files.

    Returns:
        None
    """
    file_type = 'ppar'  # Define the file type as 'ppar'
    file_path = data_folder
    current_date = time.strftime('%Y-%m-%d', time.localtime())  # Get the current date in the format 'YYYY-MM-DD'
    cate_list = os.listdir(f"{file_path}/{file_type}_category_folder")  # Get the list of files in the category folder
    df = pd.DataFrame()  # Initialize an empty DataFrame to store the data
    for file_name in cate_list:  # Iterate through each file in the category folder
        with open(os.path.join(f"{file_path}/{file_type}_category_folder", file_name), 'r') as f:  # Open the file in read mode
            doc_df = DocInfoGen(f.read())()  # Generate the document information using the DocInfoGen class
            df = pd.concat([df, doc_df])  # Concatenate the document information DataFrame to the main DataFrame
    df.to_excel(f'{data_folder}/ppar_info.xlsx')  # Save the DataFrame to an Excel file named 'ppar_info.xlsx' in the data folder
    cols = ['Proj.Id', 'doc_id', 'pdfurl']  # Specify the desired columns to keep
    df = df[cols]  # Select only the desired columns from the DataFrame
    lending = pd.read_excel('lending.xlsx', engine='openpyxl')  # Read the 'lending.xlsx' file using pandas
    pid_approval_dict = dict(lending[['Proj.Id','Approval FY']].values)  # Create a dictionary mapping project IDs to approval fiscal years
    return df

def generate_ppar_lessons_output(lessons_df, df, pid_approval_dict):
    """
    Generate PPAR lessons output and save it to an Excel file.

    Args:
        lessons_df (pandas.DataFrame): DataFrame containing PPAR lessons.
        df (pandas.DataFrame): DataFrame containing document information.
        pid_approval_dict (dict): Dictionary mapping project IDs to approval fiscal years.

    Returns:
        None
    """
    current_date = time.strftime('%m-%d-%Y', time.localtime())  # Get the current date in the format 'MM-DD-YYYY'
    output_df = lessons_df.merge(df, left_on='Project ID', right_on='Proj.Id', how='left')  # Merge the 'lessons_df' and 'df' DataFrames based on the 'Project ID' and 'Proj.Id' columns
    output_df.drop(columns=['Proj.Id'], inplace=True)  # Drop the 'Proj.Id' column from the merged DataFrame
    output_df['Project Approval FY'] = output_df['Project ID'].map(pid_approval_dict)  # Map the 'Project ID' to the corresponding approval fiscal year using 'pid_approval_dict'
    output_df.rename(columns={'Project ID': 'Project Id', 'doc_id': 'Document ID', 'pdfurl': 'Document link'}, inplace=True)  # Rename the columns as specified
    output_df['Evaluation FY'] = None  # Add a column named 'Evaluation FY' with None values
    output_df['Evaluation Date'] = None  # Add a column named 'Evaluation Date' with None values
    output_df = output_df[['Project Id', 'Project Approval FY', 'Evaluation FY', 'Evaluation Date', 'Document ID', 'Document link', 'PPAR Lessons']]  # Reorder the columns in the desired order
    # Create the output directory if it doesn't exist
    output_folder = '/Workspace/Users/mzia3@worldbank.org/PPAR'
    os.makedirs(output_folder, exist_ok=True)
    output_df.set_index('Project Id', drop=True, inplace=True)  # Set the 'Project Id' column as the index of the DataFrame
    output_df.to_excel(f'{output_folder}/ppar_lessons_{current_date}.xlsx')  # Save the DataFrame to an Excel file named 'ppar_lessons_<current_date>.xlsx' in the 'ppar_lessons_output_folder'

# COMMAND ----------

# MAGIC %md
# MAGIC #### ***Step three: Call the defined methods***

# COMMAND ----------

data_folder = '' # Provide a path to the data (download) folder
if not os.path.exists(data_folder):  # Check if the data folder exists, if not create it
    os.mkdir(data_folder)

# COMMAND ----------

file_type = ['']  # Specify the file type(s) to download, in this case, it is 'ppar'
download_version = 'txt'  # Specify the download version, it is set to 'txt' or 'pdf'
start_date = ''  # Specify the start date for downloading files, it is an empty string indicating no specific start date
end_date = ''  # Specify the end date for downloading files, it is an empty string indicating no specific end date
file_number = 999999 # Specify the number of files to download, it is not provided in the code

# Call the bulk_download_files function with the specified parameters to initiate the bulk file download
bulk_download_files(data_folder, file_type, download_version, start_date, end_date, file_number)

# COMMAND ----------

# Call the function to process PPAR lessons
lessons_df = process_ppar_lessons(data_folder)

# COMMAND ----------

# Call the function to process PPAR information and save it to an Excel file
df = process_ppar_info(data_folder)

# COMMAND ----------

# Load the 'lending.xlsx' file using pandas
lending = pd.read_excel('lending.xlsx', engine='openpyxl')

# COMMAND ----------

# Create the pid_approval_dict mapping project IDs to approval fiscal years
pid_approval_dict = dict(lending[['Proj.Id', 'Approval FY']].values)

# COMMAND ----------

# Call the function to generate PPAR lessons output and save it to an Excel file
generate_ppar_lessons_output(lessons_df, df, pid_approval_dict)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Notes:
# MAGIC ### Please make sure that bulkDownload.py, APIDocInfo.py and lending.xlsx are present in the same directory as of this code.

# COMMAND ----------

