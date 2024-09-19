

# COMMAND ----------
def read_project_ids_from_excel(excel_path, column_name='project_id'):
    try:
        df = pd.read_excel(excel_path)
        return df[column_name].dropna().tolist()
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return []

data_folder = ''  # Provide a path to the data (download) folder
excel_path = '' # Path for project_ids file
lending_path = '' # Excel Path for Lending.xlxs file
output_folder = '' # Path for the output file"
project_id = ''  # List of project IDs (column name shall be 'project_id')
file_type = ['']  # Specify the file type(s) to download, in this case, it is 'ppar'
download_version = ''  # Specify the download version, it can be set to txt or Pdf



import os, sys # Importing the 'os' module for operating system related tasks
import re  # Importing the 're' module for regular expressions
import time  # Importing the 'time' module for time-related tasks
import pandas as pd  # Importing the 'pandas' library for data manipulation
from APIDocInfo import DocInfoGen  # Importing the 'DocInfoGen' class from the 'APIDocInfo' module
from bulkDownload import bulk_download_projectID  # Importing the 'bulk_download' function from the 'BulkFilesDownload' module

def bulk_download_files(data_folder, file_type, project_id, download_version):
    """
    Bulk download files based on specified parameters.
    Args:
        data_folder (str): Path to the data folder.
        file_type (str or list): File type(s) to download.
        project_id (str or list): Project ID(s) to download.
        download_version (str): Download version.
    Returns:
    """
    # Create a dictionary with the specified parameters
    input_dict = {
    'root_path': data_folder,
    'document_type': file_type,
    'projid_list': project_id,
    'download_version': download_version
    }
    # Call the function to perform bulk file download with the input dictionary
    bulk_download_projectID(input_dict)

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
                    r'(\n+Lessons derived from the three projects.*?)Vinod Thomas'
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
            pid = pid_list[0]
            f.seek(0)  # Reset file pointer to the beginning
            text = f.read()
            if ppar_file.startswith('2018'): # Check if the file name starts with '2018'. Before 2018 format was different. 
                ccut_index = 4  # Set the cut index to 4
            cut = int(len(text) / cut_index)  # Calculate the cut position based on the cut index
            text = text[cut:]  # Remove the content before the cut position
            text = re.sub(r'\ufeff', '', text)  # Remove the Unicode BOM character
            for form in ppar_lessons_patterns_list: # Iterate through each pattern in the list
                lesson = re.findall(form, text, flags=re.I | re.S) # Find all occurrences of the pattern in the text
                if len(lesson) > 0: # If at least one match is found
                    tmp_dict = {} # Create a temporary dictionary to store the project ID and PPAR lessons
                    tmp_dict['Project ID'] = pid # Store the project ID
                    tmp_dict['PPAR Lessons'] = clean_text(lesson[0]) # Store the cleaned PPAR lesson text
                    lessons_df.append(tmp_dict) # Append the temporary dictionary to the lessons_df list
                    break
    return pd.DataFrame(lessons_df) # Create and return a DataFrame from the lessons_df list
    
def process_ppar_info(data_folder):
    """
    Process PPAR information and save it to an Excel file.

    Args:
        data_folder (str): Path to the data folder containing the PPAR files.

    Returns:
        None
    """
    file_type = 'ppar'
    file_path = data_folder
    current_date = time.strftime('%Y-%m-%d', time.localtime())
    cate_list = os.listdir(f"{file_path}/{file_type}_category_folder")  # Get the list of files in the category folder
    df = pd.DataFrame()  # Initialize an empty DataFrame to store the PPAR information
    for file_name in cate_list:  # Iterate through each file in the category folder
        with open(os.path.join(f"{file_path}/{file_type}_category_folder", file_name), 'r', encoding='utf-8', errors='ignore') as f:
            doc_df = DocInfoGen(f.read()).doc_info_gen()  # Generate document information using custom DocInfoGen class
            df = pd.concat([df, doc_df])  # Concatenate the document information DataFrame with the main DataFrame
    df.to_excel(f'{data_folder}/ppar_info.xlsx')  # Save the DataFrame to an Excel file named ppar_info.xlsx
    cols = ['Proj.Id', 'doc_id', 'pdfurl']  # Select specific columns from the DataFrame
    df = df[cols]  # Update the DataFrame with the selected columns
    lending = pd.read_excel('lending.xlsx', engine='openpyxl')  # Read the lending.xlsx file into a DataFrame
    pid_approval_dict = dict(lending[['Proj.Id', 'Approval FY']].values)  # Create a dictionary mapping project IDs to approval years
    return df  # Return the updated DataFrame
    
def generate_ppar_lessons_output(lessons_df, df, pid_approval_dict, output_folder):
    """
    Generate PPAR lessons output and save it to an Excel file.

    Args:
        lessons_df (pandas.DataFrame): DataFrame containing PPAR lessons.
        df (pandas.DataFrame): DataFrame containing document information.
        pid_approval_dict (dict): Dictionary mapping project IDs to approval fiscal years.

    Returns:
        None
    """
    current_date = time.strftime('%m-%d-%Y', time.localtime())  # Get the current date in the format 'mm-dd-yyyy'
    output_df = lessons_df.merge(df, left_on='Project ID', right_on='Proj.Id', how='left')  # Merge lessons_df and df on 'Project ID' and 'Proj.Id' columns respectively
    output_df.drop(columns=['Proj.Id'], inplace=True)  # Drop the 'Proj.Id' column from the merged DataFrame
    output_df['Project Approval FY'] = output_df['Project ID'].map(pid_approval_dict)  # Map project approval fiscal years using pid_approval_dict
    output_df.rename(columns={'Project ID': 'Project Id', 'doc_id': 'Document ID', 'pdfurl': 'Document link'}, inplace=True)  # Rename columns in the DataFrame
    output_df['Evaluation FY'] = None  # Add 'Evaluation FY' column with None values
    output_df['Evaluation Date'] = None  # Add 'Evaluation Date' column with None values
    output_df = output_df[['Project Id', 'Project Approval FY', 'Evaluation FY', 'Evaluation Date', 'Document ID', 'Document link', 'PPAR Lessons']]  # Reorder columns in the DataFrame
    # Create the output directory if it doesn't exist
    output_folder = 'ppar_lessons_output_folder'
    os.makedirs(output_folder, exist_ok=True)
    output_df.set_index('Project Id', drop=True, inplace=True)  # Set the 'Project Id' column as the index of the DataFrame
    output_df.to_excel(f'{output_folder}/ppar_lessons_{current_date}.xlsx')  # Save the DataFrame to an Excel file named 'ppar_lessons_<current_date>.xlsx' in the 'ppar_lessons_output_folder'



# COMMAND ----------

project_id = read_project_ids_from_excel(excel_path)  # List of project IDs
file_type = ['ppar']  # Specify the file type(s) to download, in this case, it is 'ppar'
download_version = 'txt'  # Specify the download version, it can be set to txt
# Call the bulk_download_files function with the specified parameters to initiate the bulk file download
bulk_download_files(data_folder, file_type, project_id, download_version)

# COMMAND ----------

# Call the function to process PPAR lessons
lessons_df = process_ppar_lessons(data_folder)

# COMMAND ----------

# Call the function to process PPAR information and save it to an Excel file
df = process_ppar_info(data_folder)

# COMMAND ----------

# Load the 'lending.xlsx' file using pandas
lending = pd.read_excel(lending_path, engine='openpyxl')

# COMMAND ----------

# Create the pid_approval_dict mapping project IDs to approval fiscal years
pid_approval_dict = dict(lending[['Proj.Id', 'Approval FY']].values)

# COMMAND ----------

# Call the function to generate PPAR lessons output and save it to an Excel file
generate_ppar_lessons_output(lessons_df, df, pid_approval_dict, output_folder)