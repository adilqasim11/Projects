#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# # 1) Import necessary libraries

# In[1]:


import PyPDF2  # Importing the PyPDF2 library for PDF processing
import pandas as pd  # Importing the pandas library for data manipulation
import pdfplumber  # Importing the pdfplumber library for PDF text extraction
import re  # Importing the re module for regular expressions
import os  # Importing the os module for operating system related tasks


# # 2) Defination of a class for extracting data from PDF files

# In[2]:


class PDFDataExtractor:
    """
    A class for extracting data from PDF files.
    """

    def __init__(self, file_path):
        """
        Initialize the PDFDataExtractor instance.

        Parameters:
        - file_path (str): The path to the PDF file.
        """
        self.file_path = file_path  # Store the file path as an instance variable
        self.pdf = pdfplumber.open(file_path)  # Open the PDF file using pdfplumber

    def extract_text_from_page(self, page_number):
        """
        Extract text from a specific page of the PDF.

        Parameters:
        - page_number (int): The page number to extract text from.

        Returns:
        - str: The extracted text.

        """
        page = self.pdf.pages[page_number]  # Get the specific page from the PDF
        return page.extract_text()  # Extract the text from the page and return it

    def extract_assessment_clr(self):
        """
        Extract the Assessment CLR section from the PDF. 
        
        Its assumed that Assessment CLR text is stored in tabular form in the PDFs. 
        So the following section of code handles the case where there is a table 
        following the Assessment CLR heading and appends the table content to the 
        extracted text.
        
        Returns:
        - str: The extracted Assessment CLR text.

        """
        found_heading = False
        assessment_clr = ""
        table_start_pattern = r"\d+\.\s"  # Pattern to identify the start of a table row
        lessons_heading = "VII. Lessons"

        for page_number, page in enumerate(self.pdf.pages):
            text = page.extract_text()
            heading_pattern = r"VI\. Assessment of CLR\n"
            match = re.search(heading_pattern, text)
            if match:
                found_heading = True
                start_index = match.end()
                assessment_clr += text[start_index:]
                break

        if found_heading:
            pdf_reader = PyPDF2.PdfReader(self.file_path)
            page_content = pdf_reader.pages[page_number].extract_text()
            table_text = re.findall(
                table_start_pattern + r".*?(?=" + table_start_pattern + "|$)",
                page_content,
                re.DOTALL,
            )
            if table_text:
                table_rows = [row.strip() for row in table_text]
                table = "\n".join(table_rows)
                assessment_clr += table

        assessment_clr_stripped = assessment_clr.strip()

        # Find the index of "Lessons" heading
        lessons_index = assessment_clr_stripped.find(lessons_heading)
        if lessons_index != -1:
            assessment_clr_stripped = assessment_clr_stripped[:lessons_index]

        # Remove the first number from the extracted paragraph
        assessment_clr_stripped = re.sub(r"^\d+\.\s", "", assessment_clr_stripped)

        return assessment_clr_stripped
   
    def extract_date(self):
        """
        Extract the date from the PDF.

        Returns:
        - str: The extracted date, or None if not found.

        """
        page_number = 0  # Assuming the date is on the first page
        text = self.extract_text_from_page(page_number) # Extracts the text from the specified page
        lines = text.split("\n") # Splits the extracted text into lines.
        if len(lines) >= 7: # Checks if the extracted text has at least 7 lines
            fourth_line = lines[6] # Retrieves the fourth line (index 6) from the extracted lines.
            date_pattern = r"\w+\s\d{1,2},\s\d{4}" # Defines a regular expression pattern to match the date format (e.g., "May 10, 2023")
            match = re.search(date_pattern, fourth_line) # Searches for a match of the date pattern in the fourth line.
            if match:
                date = match.group(0) # Retrieves the matched date string
                return date # Returns the found date
            else:
                if len(lines) >= 6: # Checks if the extracted text has at least 6 lines
                    fifth_line = lines[5] # Retrieves the fifth line (index 5) from the extracted lines.
                    match = re.search(date_pattern, fifth_line) # Searches for a match of the date pattern in the fifth line.
                    if match:
                        date = match.group(0) # Retrieves the matched date string
                        return date # Returns the found date
        return None  # Return None if date is not found

    def extract_country_name(self):
        """
        Extract the country name from the PDF. It is assumed that the country name is always on the first page.

        Returns:
        - str: The extracted country name, or None if not found.
        """
        page_number = 0  # Assuming the country name is on the first page
        text = self.extract_text_from_page(page_number) # Extracts the text from the specified page
        lines = text.split("\n") # Splits the extracted text into lines
        if len(lines) >= 5:
            second_line = lines[3]
            country_name = second_line.strip()
            if "cilbuPdezirohtuA" in country_name:
                country_name = country_name.replace("cilbuPdezirohtuA", "")

            if "Completion" in country_name:
                next_line = lines[4]
                country_name = next_line.strip()
                if "cilbuPdezirohtuA" in country_name:
                    country_name = country_name.replace("cilbuPdezirohtuA", "")

            return country_name # Returns the extracted country name

        return None  # Returns None if the country name is not found or there are less than 5 lines

    def extract_fiscal_year(self):
        """
        Extract the fiscal year from the PDF.

        Returns:
        - str: The extracted fiscal year, or None if not found.
        """
        found_heading = False
        for page in self.pdf.pages:
            if not found_heading:
                text = page.extract_text()
                heading_pattern = r'FY\d{2}-FY\d{2}'  # Regular expression pattern to match the fiscal year format (e.g., FY21-FY22)
                match = re.search(heading_pattern, text)
                if match:
                    fiscal_year = match.group()  # Extract the matched fiscal year
                    found_heading = True
                    return fiscal_year  # Return the extracted fiscal year if found
        return None  # Return None if fiscal year is not found

    def extract_lessons(self):
        """
        Extract the Lessons section from the PDF.

        Returns:
        - str: The extracted Lessons text.

        """
        found_heading = False
        lessons_text = ""  # Variable to store the lessons text

        for page in self.pdf.pages:
            text = page.extract_text()

            if not found_heading:
                heading_pattern = r"Lessons" # Expression pattern to match the start
                match = re.search(heading_pattern, text)
                if match:
                    found_heading = True
                    start_index = match.end()
                    lessons_text += text[start_index:]

            else:
                end_pattern = r"Annexes" # Expression pattern to match the end
                match = re.search(end_pattern, text)
                if match:
                    end_index = match.start()
                    lessons_text += text[:end_index]
                    break

                lessons_text += text  # Append the text to the lessons text

        # Remove numbers before and after a full stop
        lessons_text = re.sub(r"\b\d+\.\s+|\s+\d+\.\b", "", lessons_text)

        return lessons_text # Return the lessons text

    def extract_executive_summary(self):
        """
        Extract the Executive Summary section from the PDF.

        Returns:
        - str: The extracted Executive Summary text.

        """
        found_heading = False
        summary_text = ""  # Variable to store the summary text

        for page in self.pdf.pages:
            text = page.extract_text()

            if not found_heading:
                heading_pattern = r"Executive Summary" # Expression pattern to match the "Executive Summary" heading
                match = re.search(heading_pattern, text)
                if match:
                    found_heading = True
                    start_index = match.end()
                    summary_text += text[start_index:]

            else:
                end_pattern = r"II\." # Expression pattern to match the end of the Executive Summary section

                match = re.search(end_pattern, text)
                if match:
                    end_index = match.start()
                    summary_text += text[:end_index]
                    return summary_text

                summary_text += text  # Append the text to the summary text

        return summary_text # Return the summary text

    def extract_strategic_focus(self):
        """
        Extract the Strategic Focus section from the PDF.

        Returns:
        - str: The extracted Strategic Focus text.
        """
        found_heading = False
        strategic_text = ""  # Variable to store the strategic focus text

        for page in self.pdf.pages:
            if not found_heading:
                text = page.extract_text()
                heading_pattern = r"Strategic Focus"  # Regular expression pattern to match the "Strategic Focus" heading
                match = re.search(heading_pattern, text)
                if match:
                    found_heading = True
                    start_index = match.end()
                    strategic_text = text[start_index:]
            else:
                text = page.extract_text()
                end_pattern = r"III\."  # Regular expression pattern to match the end of the Strategic Focus section
                match = re.search(end_pattern, text)
                if match:
                    end_index = match.start()
                    strategic_text += text[:end_index]
                    break
                else:
                    strategic_text += text

        return strategic_text # Return the strategic text

    def extract_word_after_heading(self, heading_pattern):
        """
        Extract the text following a specific heading pattern.

        Parameters:
        - heading_pattern (str): The regular expression pattern for the heading.

        Returns:
        - str: The extracted text following the heading.

        """
        found_heading = False
        extracted_text = ""

        for page in self.pdf.pages:
            if not found_heading:
                text = page.extract_text()
                match = re.search(heading_pattern, text)  # Search for the specified heading pattern in the extracted text
                if match:
                    found_heading = True
                    start_index = match.end()  # Determine the index following the matched heading
                    remaining_text = text[start_index:]  # Extract the text following the heading
                    punctuation_match = re.search(r"[.,]", remaining_text)  # Search for punctuation marks
                    if punctuation_match:
                        end_index = punctuation_match.start()  # Determine the index of the punctuation mark
                        extracted_text = remaining_text[:end_index]  # Extract the text up to the punctuation mark
                    else:
                        extracted_text = remaining_text
                    break  # Stop iterating over pages once the heading is found

        return extracted_text # Return the extracted text

    def extract_overall_assessment(self):
        """
        Extract the overall assessment from the PDF.

        Returns:
        - str: The extracted overall assessment.

        """
        heading_pattern = r"development outcome as"  # Regular expression pattern for the specific heading to search for
        return self.extract_word_after_heading(heading_pattern)  # Call the extract_word_after_heading method with the specified heading pattern
    

    def extract_development_outcome(self):
        """
        Extract the Development Outcome section from the PDF.

        Returns:
        - str: The extracted Development Outcome text.
        """
        found_heading = False
        development_text = ""  # Variable to store the strategic focus text

        for page_number, page in enumerate(self.pdf.pages):
            if not found_heading:
                text = page.extract_text()
                heading_pattern = r"IV\. Development Outcome\n"  # Regular expression pattern to match the "Development Outcome" heading
                match = re.search(heading_pattern, text)
                if match:
                    found_heading = True
                    start_index = match.end()
                    development_text += text[start_index:]
            else:
                text = page.extract_text()
                end_pattern = r"V\."  # Regular expression pattern to match the end of the Development Outcome section
                match = re.search(end_pattern, text)
                if match:
                    end_index = match.start()
                    development_text += text[:end_index]
                    break
                else:
                    development_text += text

        return development_text  # Return the development outcome text

    def extract_WBG_performance(self):
        """
        Extract the WBG performance from the PDF.

        Returns:
        - str: The extracted WBG performance text.
        """
        found_heading = False
        WBG_performance_text = ""  # Variable to store the strategic focus text

        for page in self.pdf.pages:
            if not found_heading:
                text = page.extract_text()
                heading_pattern = r"V. WBG Performance"  # Regular expression pattern to match the "Development Outcome" heading
                match = re.search(heading_pattern, text)
                if match:
                    found_heading = True
                    start_index = match.end()
                    WBG_performance_text = text[start_index:]
            else:
                text = page.extract_text()
                end_pattern = r"VI\."  # Regular expression pattern to match the end of the Development Outcome section
                match = re.search(end_pattern, text)
                if match:
                    end_index = match.start()
                    WBG_performance_text += text[:end_index]
                    break
                else:
                    WBG_performance_text += text

        return WBG_performance_text # Return the strategic text
    
    def close(self):
        """
        Close the opened PDF file.

        """
        self.pdf.close()
        

