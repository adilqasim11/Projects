#!/usr/bin/env python
# coding: utf-8

# ### 1) Run this part if there are only Primary keywords

# In[11]:


import string
import os
import re
import nltk
import csv
from nltk.tokenize import PunktSentenceTokenizer
from tika import parser

data = []

def count_sentences(text):
    sentence_endings = ['.', '!', '?']
    sentence_count = 0
    for char in text:
        if char in sentence_endings:
            sentence_count += 1
    return sentence_count

def extract_project_ids_from_folder(folder_path):
    project_ids = {}
    file_names = os.listdir(folder_path)
    for file_name in file_names:
        match = re.search(r"_(P\d{6})", file_name)
        if match:
            project_id = match.group(1)
            project_ids[file_name] = project_id
        else:
            file_path = os.path.join(folder_path, file_name)
            if file_name.endswith('.txt'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                        match = re.search(r"P\d{6}", text)
                        if match:
                            project_id = match.group()
                            project_ids[file_name] = project_id
                except UnicodeDecodeError:
                    print('')
            elif file_name.endswith('.pdf'):
                try:
                    raw = parser.from_file(os.path.join(folder_path, file_name))
                    text = raw['content']
                    match = re.search(r"P\d{6}", text)
                    if match:
                        project_id = match.group()
                        project_ids[file_name] = project_id
                except Exception as e:
                    print(f"Error while processing {file_name}: {e}")
    return project_ids

def clean(bad_text):
    remove_patterns = [ 
        r'^\d+$|Page \d+ of \d+',
        r'Page \d+',
        r'Page \d+ of \d+',
        r'The World Bank\s+(.*?)\s+\(P\d+\)',
        r'(\d+)\s+of\s+(\d+)',
        r'The World Bank.*?\(P\d{6}\)'
    ]
    combined_pattern = '|'.join(remove_patterns)
    good_text = re.sub(combined_pattern, '', bad_text, flags=re.MULTILINE)
    return good_text

def remove_table_of_contents(text):
    pattern = r"Table of Contents|Contents|TABLE OF CONTENTS|CONTENTS"
    characters_to_remove = 14000
    match = re.search(pattern, text, re.IGNORECASE)
    
    if match:
        start_position = match.end()
        new_text = text[:start_position] + text[start_position + characters_to_remove:]
        return new_text
    else:
        return text

def extract_context_text(folder_path, primary_keywords):
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except LookupError:
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
    
    project_ids = extract_project_ids_from_folder(folder_path)
    tokenizer = PunktSentenceTokenizer()

    for filename, project_id in project_ids.items():
        if filename.endswith(".txt"):
            file = os.path.join(folder_path, filename)
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    text = f.read()
                    text = remove_table_of_contents(text)
                    text = clean(text)
                    sentences = tokenizer.tokenize(text)
                    for primary_keyword in primary_keywords:
                        keyword_pairs = [(primary_keyword, None)]
                        for keyword_pair in keyword_pairs:
                            keyword = keyword_pair[0]
                            verb = keyword_pair[1]
                            keyword_pattern = re.escape(keyword)
                            for sentence in sentences:
                                if re.search(keyword_pattern, sentence, re.IGNORECASE):
                                    tagged_words = nltk.pos_tag(nltk.word_tokenize(sentence))
                                    index = sentences.index(sentence)

                                    # Collecting sentences before the keyword sentence
                                    before_context = []
                                    found_sentences = 0
                                    for i in range(index - 1, -1, -1):
                                        if found_sentences >= 2:
                                            break
                                        if len(sentences[i].split()) > 4:
                                            before_context.insert(0, sentences[i])
                                            found_sentences += 1
                                        else:
                                            before_context.insert(0, sentences[i])

                                    # Collecting sentences after the keyword sentence
                                    after_context = []
                                    found_sentences = 0
                                    for i in range(index + 1, len(sentences)):
                                        if found_sentences >= 2:
                                            break
                                        if len(sentences[i].split()) > 4:
                                            after_context.append(sentences[i])
                                            found_sentences += 1
                                        else:
                                            after_context.append(sentences[i])

                                    # Combine the context
                                    context = before_context + [sentence] + after_context

                                    # Ensure exactly 5 sentences with more than 4 words
                                    context_with_required_sentences = []
                                    for sent in context:
                                        if len(sent.split()) > 4 or len(context_with_required_sentences) < 5:
                                            context_with_required_sentences.append(sent)
                                    context = ' '.join(context_with_required_sentences)

                                    data.append([project_id, keyword, context])
                                    # Your existing processing code here
                                    
                                    print("Found in text file:", filename)
                                    print("Project ID:", project_id)
                                    print("Keyword:", keyword)
                                    print("Sentence:", sentence)
                                    print("-------")
                                    pass
            except UnicodeDecodeError:
                print('---')
        elif filename.endswith(".pdf"):
            file = os.path.join(folder_path, filename)
            try:
                raw = parser.from_file(file)
                text = raw['content']
                text = remove_table_of_contents(text)
                text = clean(text)
                sentences = tokenizer.tokenize(text)
                for primary_keyword in primary_keywords:
                    keyword_pairs = [(primary_keyword, None)]
                    for keyword_pair in keyword_pairs:
                        keyword = keyword_pair[0]
                        verb = keyword_pair[1]
                        keyword_pattern = re.escape(keyword)
                        for sentence in sentences:
                            if re.search(keyword_pattern, sentence, re.IGNORECASE):
                                tagged_words = nltk.pos_tag(nltk.word_tokenize(sentence))


     
                                index = sentences.index(sentence)

                                    # Collecting sentences before the keyword sentence
                                before_context = []
                                found_sentences = 0
                                for i in range(index - 1, -1, -1):
                                    if found_sentences >= 2:
                                        break
                                    if len(sentences[i].split()) > 4:
                                        before_context.insert(0, sentences[i])
                                        found_sentences += 1
                                    else:
                                        before_context.insert(0, sentences[i])

                                    # Collecting sentences after the keyword sentence
                                after_context = []
                                found_sentences = 0
                                for i in range(index + 1, len(sentences)):
                                    if found_sentences >= 2:
                                        break
                                    if len(sentences[i].split()) > 4:
                                        after_context.append(sentences[i])
                                        found_sentences += 1
                                    else:
                                        after_context.append(sentences[i])

                                    # Combine the context
                                context = before_context + [sentence] + after_context

                                    # Ensure exactly 5 sentences with more than 4 words
                                context_with_required_sentences = []
                                for sent in context:
                                    if len(sent.split()) > 4 or len(context_with_required_sentences) < 5:
                                        context_with_required_sentences.append(sent)
                                context = ' '.join(context_with_required_sentences)

                                data.append([project_id, keyword, context])
                                # Your existing processing code here
                                print("Found in PDF file:", filename)
                                print("Project ID:", project_id)
                                print("Keyword:", keyword)
                                print("Sentence:", sentence)
                                print("-------")
                                pass
            except Exception as e:
                print(f"Error while processing {filename}: {e}")

    return data



# Ensure the paths are raw strings
folder_path = r"" # Path containg the txt files
keywords_excel_path = r".xlsx"
output_path = r".xlsx"
output_pickle_path = r".pkl"


# Read primary keywords from Excel file
primary_keywords_df = pd.read_excel(keywords_excel_path)
primary_keywords = primary_keywords_df["Primary Keyword"].tolist()

data = extract_context_text(folder_path, primary_keywords)

# Create a DataFrame
df = pd.DataFrame(data, columns=['Project ID', 'Primary Keyword', 'Relevant Text'])

# Save DataFrame to Excel
df.to_excel(output_path, index=False)


print(f'Data has been saved to {output_path}')

# Save DataFrame to pickle
with open(output_pickle_path, 'wb') as f:
    pickle.dump(df, f)
print(f'Data has been saved to {output_pickle_path}')


# ### 2) Run this part for a list of primary and secondary keywords

# In[10]:


import os
import re
import nltk
import pandas as pd
from nltk.tokenize import PunktSentenceTokenizer
from tika import parser
import pickle

data = []

def count_sentences(text):
    sentence_endings = ['.', '!', '?']
    sentence_count = 0
    for char in text:
        if char in sentence_endings:
            sentence_count += 1
    return sentence_count

def extract_project_ids_from_folder(folder_path):
    project_ids = {}
    file_names = os.listdir(folder_path)
    for file_name in file_names:
        match = re.search(r"_(P\d{6})", file_name)
        if match:
            project_id = match.group(1)
            project_ids[file_name] = project_id
        else:
            file_path = os.path.join(folder_path, file_name)
            if file_name.endswith('.txt'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                        match = re.search(r"P\d{6}", text)
                        if match:
                            project_id = match.group()
                            project_ids[file_name] = project_id
                except UnicodeDecodeError:
                    print('')
            elif file_name.endswith('.pdf'):
                try:
                    raw = parser.from_file(os.path.join(folder_path, file_name))
                    text = raw['content']
                    match = re.search(r"P\d{6}", text)
                    if match:
                        project_id = match.group()
                        project_ids[file_name] = project_id
                except Exception as e:
                    print(f"Error while processing {file_name}: {e}")
    return project_ids

def clean(bad_text):
    remove_patterns = [ 
        r'^\d+$|Page \d+ of \d+',
        r'Page \d+',
        r'Page \d+ of \d+',
        r'The World Bank\s+(.*?)\s+\(P\d+\)',
        r'(\d+)\s+of\s+(\d+)',
        r'The World Bank.*?\(P\d{6}\)'
    ]
    combined_pattern = '|'.join(remove_patterns)
    good_text = re.sub(combined_pattern, '', bad_text, flags=re.MULTILINE)
    return good_text
    
def remove_table_of_contents(text):
    pattern = r"Table of Contents|Contents|TABLE OF CONTENTS|CONTENTS"
    characters_to_remove = 14000
    match = re.search(pattern, text, re.IGNORECASE)
    
    if match:
        start_position = match.end()
        new_text = text[:start_position] + text[start_position + characters_to_remove:]
        return new_text
    else:
        return text

def extract_keywords_from_excel(file_path):
    keywords_df = pd.read_excel(file_path)
    keyword_pairs = []
    for index, row in keywords_df.iterrows():
        primary_keyword = str(row['Primary Keyword'])  # Convert to string
        secondary_keyword = str(row['Secondary Keyword'])  # Convert to string
        keyword_pairs.append((primary_keyword, secondary_keyword))
    return keyword_pairs



def extract_context_text(file_path, primary_keyword, secondary_keywords):
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except LookupError:
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')

    project_ids = extract_project_ids_from_folder(file_path)
    tokenizer = PunktSentenceTokenizer()

    all_data = []  # Initialize an empty list to collect data

    # Split primary and secondary keywords
    primary_keywords = primary_keyword.split(',')
    secondary_keywords = secondary_keywords.split(',')

    # Iterate over each keyword pair
    for primary_kw, secondary_kw in zip(primary_keywords, secondary_keywords):
        primary_kw = primary_kw.strip()
        secondary_kw = secondary_kw.strip()

        print("Current Keyword Pair:", primary_kw, secondary_kw)  # Debugging line

        keyword_data = []  # Initialize a list to collect data for the current keyword pair

        # Iterate over files and extract data for the current keyword pair
        for filename, project_id in project_ids.items():
            file = os.path.join(file_path, filename)
            if file.endswith(".txt"):
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        text = f.read()
                        text = remove_table_of_contents(text)
                        text = clean(text)
                        sentences = tokenizer.tokenize(text)
                        for sentence in sentences:
                            if re.search(re.escape(primary_kw), sentence, re.IGNORECASE) and re.search(
                                    re.escape(secondary_kw), sentence, re.IGNORECASE):
                                print("Primary Keyword Found:", primary_kw)  # Debugging line
                                print("Secondary Keyword Found:", secondary_kw)  # Debugging line
                                print("Sentence:", sentence)  # Debugging line
                                real_sentence = sentence
                                tagged_words = nltk.pos_tag(nltk.word_tokenize(sentence))
                                associated_verb = None
                                for word, pos in tagged_words:
                                    if pos.startswith('VB') and word.lower() not in ['is', 'was', 'be', 's',
                                                                                        'has', 'have', '"',
                                                                                        'are']:
                                        associated_verb = word
                                        break
                                index = sentences.index(sentence)

                                # Collecting sentences before the keyword sentence
                                before_context = []
                                found_sentences = 0
                                for i in range(index - 1, -1, -1):
                                    if found_sentences >= 2:
                                        break
                                    if len(sentences[i].split()) > 4:
                                        before_context.insert(0, sentences[i])
                                        found_sentences += 1
                                    else:
                                        before_context.insert(0, sentences[i])

                                # Collecting sentences after the keyword sentence
                                after_context = []
                                found_sentences = 0
                                for i in range(index + 1, len(sentences)):
                                    if found_sentences >= 2:
                                        break
                                    if len(sentences[i].split()) > 4:
                                        after_context.append(sentences[i])
                                        found_sentences += 1
                                    else:
                                        after_context.append(sentences[i])

                                # Combine the context
                                context = before_context + [sentence] + after_context

                                # Ensure exactly 5 sentences with more than 4 words
                                context_with_required_sentences = []
                                for sent in context:
                                    if len(sent.split()) > 4 or len(context_with_required_sentences) < 5:
                                        context_with_required_sentences.append(sent)
                                context = ' '.join(context_with_required_sentences)

                                secondary_keyword_pattern = re.escape(secondary_kw) + r'|\b\w*{}\w*\b'.format(re.escape(secondary_kw))
                                # Calculate distance
                                content = context
                                reference_sentence = sentence
                                primary_indices = []

                                # Split the content by '.' to iterate over each sentence
                                for sentence in content.split('.'):
                                    if primary_kw in sentence and primary_kw in reference_sentence:
                                        # Find the index of the keyword within the sentence
                                        index_within_sentence = sentence.find(primary_kw)
                                        if index_within_sentence != -1:
                                            # Calculate the index within the entire content and append to the list
                                            primary_indices.append(content.find(sentence) + index_within_sentence)
                                            break  # stop searching after finding the first occurrence

                                print(primary_indices)

                                
                                
                                secondary_indices = [m.start() for m in re.finditer(secondary_keyword_pattern, content)]

                                # Debugging lines
                                print("Primary Indices:", primary_indices)
                                print("Secondary Indices:", secondary_indices)

                                if isinstance(primary_indices, int):
                                    primary_indices = [primary_indices]

                                for primary_index in primary_indices:
                                    for secondary_index in secondary_indices:
                                        # Calculate the distance between primary and secondary keyword occurrences
                                        distance = secondary_index - primary_index
                                        print(distance)
                                        #distance = -distance  # Taking absolute distance
                                        keyword_data.append([project_id, primary_kw, secondary_kw, distance, sentence, content])

                except UnicodeDecodeError:
                    print('---')
                    
            elif file.endswith(".pdf"):
                try:
                    with open(file, 'rb') as f:
                        raw = parser.from_file(file)
                        text = raw['content']
                        text = remove_table_of_contents(text)
                        text = clean(text)
                        sentences = tokenizer.tokenize(text)
                        for sentence in sentences:
                            if re.search(re.escape(primary_kw), sentence, re.IGNORECASE) and re.search(
                                    re.escape(secondary_kw), sentence, re.IGNORECASE):
                                print("Primary Keyword Found:", primary_kw)  # Debugging line
                                print("Secondary Keyword Found:", secondary_kw)  # Debugging line
                                print("Sentence:", sentence)  # Debugging line
                                real_sentence = sentence
                                tagged_words = nltk.pos_tag(nltk.word_tokenize(sentence))
                                associated_verb = None
                                for word, pos in tagged_words:
                                    if pos.startswith('VB') and word.lower() not in ['is', 'was', 'be', 's',
                                                                                        'has', 'have', '"',
                                                                                        'are']:
                                        associated_verb = word
                                        break
                                index = sentences.index(sentence)

                                # Collecting sentences before the keyword sentence
                                before_context = []
                                found_sentences = 0
                                for i in range(index - 1, -1, -1):
                                    if found_sentences >= 2:
                                        break
                                    if len(sentences[i].split()) > 4:
                                        before_context.insert(0, sentences[i])
                                        found_sentences += 1
                                    else:
                                        before_context.insert(0, sentences[i])

                                # Collecting sentences after the keyword sentence
                                after_context = []
                                found_sentences = 0
                                for i in range(index + 1, len(sentences)):
                                    if found_sentences >= 2:
                                        break
                                    if len(sentences[i].split()) > 4:
                                        after_context.append(sentences[i])
                                        found_sentences += 1
                                    else:
                                        after_context.append(sentences[i])

                                # Combine the context
                                context = before_context + [sentence] + after_context

                                # Ensure exactly 5 sentences with more than 4 words
                                context_with_required_sentences = []
                                for sent in context:
                                    if len(sent.split()) > 4 or len(context_with_required_sentences) < 5:
                                        context_with_required_sentences.append(sent)
                                context = ' '.join(context_with_required_sentences)

                                secondary_keyword_pattern = re.escape(secondary_kw) + r'|\b\w*{}\w*\b'.format(re.escape(secondary_kw))
                                # Calculate distance
                                content = context
                                reference_sentence = sentence
                                primary_indices = []

                                # Split the content by '.' to iterate over each sentence
                                for sentence in content.split('.'):
                                    if primary_kw in sentence and primary_kw in reference_sentence:
                                        # Find the index of the keyword within the sentence
                                        index_within_sentence = sentence.find(primary_kw)
                                        if index_within_sentence != -1:
                                            # Calculate the index within the entire content and append to the list
                                            primary_indices.append(content.find(sentence) + index_within_sentence)
                                            break  # stop searching after finding the first occurrence

                                print(primary_indices)

                                
                                
                                secondary_indices = [m.start() for m in re.finditer(secondary_keyword_pattern, content)]

                                # Debugging lines
                                print("Primary Indices:", primary_indices)
                                print("Secondary Indices:", secondary_indices)

                                if isinstance(primary_indices, int):
                                    primary_indices = [primary_indices]

                                for primary_index in primary_indices:
                                    for secondary_index in secondary_indices:
                                        # Calculate the distance between primary and secondary keyword occurrences
                                        distance = secondary_index - primary_index
                                        print(distance)
                                        #distance = -distance  # Taking absolute distance
                                        keyword_data.append([project_id, primary_kw, secondary_kw, distance, sentence, content])

                        # Rest of your processing for PDF files...
                except Exception as e:
                    print(f"Error while processing {filename}: {e}")

            print("Length of keyword_data for", filename, ":", len(keyword_data))  # Debugging line

        # Append data for the current keyword pair to the main list
        all_data.extend(keyword_data)

    return all_data


keywords_file = ".xlsx" # Path to keywords files
folder_path = "" # Path to folder containing data (txt) files
output_path = ".xlsx" # To save the result in a excel file
output_pickle_path = ".pkl" #Path of the output pickle file



keyword_pairs = extract_keywords_from_excel(keywords_file)

if folder_path and output_path and keyword_pairs:
    # Create a DataFrame to store the extracted data
    all_data_df = pd.DataFrame(columns=['Project ID', 'Primary Keyword', 'Secondary Keyword', 'Distance' , 'Main Sentence', 'Text'])

    for primary_keyword, secondary_keyword in keyword_pairs:  # Iterate over keyword pairs
        extracted_data = extract_context_text(folder_path, primary_keyword, secondary_keyword)  # Extract data for current keyword pair
        # Append the extracted data to the DataFrame
        all_data_df = all_data_df.append(pd.DataFrame(extracted_data, columns=['Project ID', 'Primary Keyword', 'Distance','Secondary Keyword', 'Main Sentence', 'Text']), ignore_index=True)

    # Save the DataFrame to an Excel file
    all_data_df.to_excel(output_path, index=False)
    print(f'Data has been saved to {output_path}')
    
    # Save the DataFrame to a pickle file
    with open(output_pickle_path, 'wb') as f:
        pickle.dump(all_data_df, f)
    print(f'Data has been saved to {output_pickle_path}')
else:
    print("Please provide all necessary inputs.")


# ### Displaying the result from pickle file

# In[12]:


# Load data from pickle file
with open(output_pickle_path, 'rb') as f:
    data = pickle.load(f)

# Display the data
print(data)


# In[ ]:




