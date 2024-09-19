# Databricks notebook source
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import Libraries
from datetime import datetime
import pandas as ps

# Load DataHub Extract Tabs into DataFrame (to be replaced with a direct connection to the DataLake)
# Define the sheet name and index column for loading data
sheet_name = 'Export'
index_col = 'Project Id'

# Loading various Excel files into pandas DataFrames
# These files contain different project data and related information
with ps.ExcelFile('1.a Project Data.xlsx') as xlsx: dh_extract_1a = ps.read_excel(xlsx, sheet_name=sheet_name, index_col=index_col, keep_default_na=False, dtype=str)
with ps.ExcelFile('1.b Project Data.xlsx') as xlsx: dh_extract_1b = ps.read_excel(xlsx, sheet_name=sheet_name, keep_default_na=False, dtype=str)
with ps.ExcelFile('3.a Rel. of Objectives.xlsx') as xlsx: dh_extract_3a = ps.read_excel(xlsx, sheet_name=sheet_name, index_col=index_col, keep_default_na=False, dtype=str)
with ps.ExcelFile('5 Efficiency.xlsx') as xlsx: dh_extract_5 = ps.read_excel(xlsx, sheet_name=sheet_name, index_col=index_col, keep_default_na=False, dtype=str)
with ps.ExcelFile('8 Bank Performance.xlsx') as xlsx: dh_extract_8 = ps.read_excel(xlsx, sheet_name=sheet_name, index_col=index_col, keep_default_na=False, dtype=str)
with ps.ExcelFile('9 Browser Performance.xlsx') as xlsx: dh_extract_9 = ps.read_excel(xlsx, sheet_name=sheet_name, index_col=index_col, keep_default_na=False, dtype=str)
with ps.ExcelFile('12 Ratings.xlsx') as xlsx: dh_extract_12 = ps.read_excel(xlsx, sheet_name=sheet_name, index_col=index_col, keep_default_na=False, dtype=str)

# Remove duplicate Project IDs from dh_extract_1b and set its index
dh_extract_1b.drop_duplicates(subset=[index_col], inplace=True)
dh_extract_1b.set_index(index_col, inplace=True)

# Load List of ProjectIds from DataHub (Tab 1b)
pid_list = dh_extract_1b.index
# pid_list = ['P131763', 'P133738', 'P132786', 'P146665', 'P146243', 'P149781', 'P147557', 'P151620', 'P147806', 'P157469', 'P150313', 'P151479', 'P150677', 'P151941']

# Define columns for the output report and create an empty DataFrame for it
output_cols = [index_col, 'Test Results', 'Prog DPF Member Type', 'Series First Project Id', 'Outcome', 'Outcome Parent', 'Rel Obj',  'Rel Obj Parent',  'Rev Rel Obj',  'Rev Rel Obj Parent', 'Rel Design',  'Rel Design Parent',  'Rev Rel Design',  'Rev Design Obj Parent', 'Rel Prior Act',  'Rel Prior Act Parent',  'Rel Res Ind',  'Rel Res Ind Parent',  'Efficiency', 'Efficiency Parent', 'RDO', 'RDO Parent', 'Bank Perf', 'Bank Perf Parent', 'QaE', 'QaE Parent', 'QoS', 'QoS Parent', 'Borr Perf', 'Borr Perf Parent', 'Govt Perf', 'Govt Perf Parent', 'Imp Agcy Perf', 'Imp Agcy Perf Parent', 'ME Qty', 'ME Qty Parent', 'ICR Qty', 'ICR Qty Parent']
output = ps.DataFrame(columns=output_cols)
output_row = ps.DataFrame(columns=output_cols)

# Function to get ProjectId Instrument Type from dh_extract_1a
def get_pid_inst_type(pid):
    return dh_extract_1a.loc[pid].get('Instrument Type Name')

# Function to check if a ProjectId is part of a DPF Series
def pid_in_dpf_series(pid):
    return pid in dh_extract_1b.index

# Main loop to process each ProjectId
for pid in pid_list:
    # Extracting various types of information for each ProjectId
    # This includes member type, series first project id, parent project id, etc.
    pid_rtg_dict = {'outcome':'', 'rel_obj':'', 'rev_rel_obj':'', 'rel_design':'', 'rev_rel_design':'', 'rel_prior_act':'', 'rel_res_ind':'', 'efficiency':'', 'rdo':'', 'bank_perf':'', 'qae':'', 'qos':'', 'borr_perf':'', 'govt_perf':'', 'imp_agcy_perf':'', 'me_qty':'', 'icr_qty':''}
    prnt_rtg_dict = {'outcome':'', 'rel_obj':'', 'rev_rel_obj':'', 'rel_design':'', 'rev_rel_design':'', 'rel_prior_act':'', 'rel_res_ind':'', 'efficiency':'', 'rdo':'', 'bank_perf':'', 'qae':'', 'qos':'', 'borr_perf':'', 'govt_perf':'', 'imp_agcy_perf':'', 'me_qty':'', 'icr_qty':''}

    member_type = dh_extract_1b.loc[pid].get('Programmatic DPF Member Type')
    series_first_pid = dh_extract_1b.loc[pid].get('Programmatic DPF Series Project Leader')
    parent_pid = dh_extract_1b.loc[pid].get('Parent Project Id')

    return_message = ''
    output_results = 'Check: '
    
    print(f"\nProjectID: {pid}")
    print('------------------')

    # Check if ProjectId exists in various data extracts and retrieve related information
    # This block of code checks multiple data extracts (e.g., dh_extract_12, dh_extract_3a, etc.)
    # and extracts relevant ratings and information for each ProjectId.
    # If a ProjectId is not found in a specific extract, it skips to the next iteration.
    if pid in dh_extract_12.index:
        pid_rtg_dict['outcome'] = dh_extract_12.loc[pid].get('Outcome Rating')
        pid_rtg_dict['bank_perf'] = dh_extract_12.loc[pid].get('Overall Bank Performance Rating')
        pid_rtg_dict['borr_perf'] = dh_extract_12.loc[pid].get('Overall Borrower Performance Rating')
        pid_rtg_dict['rdo'] = dh_extract_12.loc[pid].get('Risk To Development Outcome Rating')
        pid_rtg_dict['me_qty'] = dh_extract_12.loc[pid].get('ME Quality Rating')
        pid_rtg_dict['icr_qty'] = dh_extract_12.loc[pid].get('ICR Quality Rating')
    else:
        print(f"ProjectID {pid} not found in dh_extract_12")
        continue  # Skip this iteration

    if pid in dh_extract_3a.index:
        pid_rtg_dict['rel_obj'] = dh_extract_3a.loc[pid].get('Relevance Of Objective Rating')
        pid_rtg_dict['rev_rel_obj'] = dh_extract_3a.loc[pid].get('Revised Relevance Of Objectives Rating')
        pid_rtg_dict['rel_design'] = dh_extract_3a.loc[pid].get('Relevance Of Design Rating')
        pid_rtg_dict['rev_rel_design'] = dh_extract_3a.loc[pid].get('Revised Relevance Of Design Rating')
        pid_rtg_dict['rel_prior_act'] = dh_extract_3a.loc[pid].get('Relevance of Prior Action Rating')
        pid_rtg_dict['rel_res_ind'] = dh_extract_3a.loc[pid].get('Relevance of Results Rating')
        # ... other assignments for dh_extract_3a ...
    else:
        print(f"ProjectID {pid} not found in dh_extract_3a")
        continue

    if pid in dh_extract_5.index:
        pid_rtg_dict['efficiency'] = dh_extract_5.loc[pid].get('Efficiency Rating')
    else:
        print(f"ProjectID {pid} not found in dh_extract_5")
        continue
        
 # Check for dh_extract_8
    if pid in dh_extract_8.index:
        pid_rtg_dict['qae'] = dh_extract_8.loc[pid].get('Quality At Entry Rating')
        pid_rtg_dict['qos'] = dh_extract_8.loc[pid].get('Quality At Supervision Rating')
    else:
        print(f"ProjectID {pid} not found in dh_extract_8")
        continue

    # Check for dh_extract_9
    if pid in dh_extract_9.index:
        pid_rtg_dict['govt_perf'] = dh_extract_9.loc[pid].get('Government Performance Rating')
        pid_rtg_dict['imp_agcy_perf'] = dh_extract_9.loc[pid].get('Implementing Agency Performance Rating')
    else:
        print(f"ProjectID {pid} not found in dh_extract_9")
        continue
        
    # Special handling for 'First' member type in a DPF Series
    if member_type == 'First':
        output_results = 'Series First ProjectId'
        return_message += 'Series First ProjectId'
        # Populating the output_row DataFrame with extracted data
        output_row.loc[0] = [pid, output_results, member_type, series_first_pid, pid_rtg_dict['outcome'], '', pid_rtg_dict['rel_obj'], '', pid_rtg_dict['rev_rel_obj'], '', pid_rtg_dict['rel_design'], '', pid_rtg_dict['rev_rel_design'], '', pid_rtg_dict['rel_prior_act'], '', pid_rtg_dict['rel_res_ind'], '', pid_rtg_dict['efficiency'], '', pid_rtg_dict['rdo'], '', pid_rtg_dict['bank_perf'], '', pid_rtg_dict['qae'], '', pid_rtg_dict['qos'], '', pid_rtg_dict['borr_perf'], '', pid_rtg_dict['govt_perf'], '', pid_rtg_dict['imp_agcy_perf'], '', pid_rtg_dict['me_qty'], '', pid_rtg_dict['icr_qty'], '']
    else:
        # Additional data extraction and comparison for series_first_pid
        # This part compares the ratings of the current ProjectId with its parent (series_first_pid)
        if series_first_pid in dh_extract_12.index:
            prnt_rtg_dict['outcome'] = dh_extract_12.loc[series_first_pid].get('Outcome Rating')
            prnt_rtg_dict['rdo'] = dh_extract_12.loc[series_first_pid].get('Risk To Development Outcome Rating')
            prnt_rtg_dict['borr_perf'] = dh_extract_12.loc[series_first_pid].get('Overall Borrower Performance Rating')
            prnt_rtg_dict['bank_perf'] = dh_extract_12.loc[series_first_pid].get('Overall Bank Performance Rating')
            prnt_rtg_dict['me_qty'] = dh_extract_12.loc[series_first_pid].get('ME Quality Rating')
            prnt_rtg_dict['icr_qty'] = dh_extract_12.loc[series_first_pid].get('ICR Quality Rating')
        else:
            print(f"Series First ProjectID {series_first_pid} not found in dh_extract_12")
            continue
        if series_first_pid in dh_extract_3a.index:
            prnt_rtg_dict['rel_obj'] = dh_extract_3a.loc[series_first_pid].get('Relevance Of Objective Rating')
            prnt_rtg_dict['rev_rel_obj'] = dh_extract_3a.loc[series_first_pid].get('Revised Relevance Of Objectives Rating')
            prnt_rtg_dict['rel_design'] = dh_extract_3a.loc[series_first_pid].get('Relevance Of Design Rating')
            prnt_rtg_dict['rev_rel_design'] = dh_extract_3a.loc[series_first_pid].get('Revised Relevance Of Design Rating')
            prnt_rtg_dict['rel_prior_act'] = dh_extract_3a.loc[series_first_pid].get('Relevance of Prior Action Rating')
            prnt_rtg_dict['rel_res_ind'] = dh_extract_3a.loc[series_first_pid].get('Relevance of Results Rating')
            # ... other assignments for series_first_pid ...
        else:
            print(f"Series First ProjectID {series_first_pid} not found in dh_extract_3a")
            continue
        if series_first_pid in dh_extract_5.index:
            prnt_rtg_dict['efficiency'] = dh_extract_5.loc[series_first_pid].get('Efficiency Rating')
        else:
            print(f"Series First ProjectID {series_first_pid} not found in dh_extract_5")
            continue 
        if series_first_pid in dh_extract_8.index:
            prnt_rtg_dict['qae'] = dh_extract_8.loc[series_first_pid].get('Quality At Entry Rating')
            prnt_rtg_dict['qos'] = dh_extract_8.loc[series_first_pid].get('Quality At Supervision Rating')
        else:
            print(f"Series First ProjectID {series_first_pid} not found in dh_extract_8")
            continue 
    
        if series_first_pid in dh_extract_9.index:
            prnt_rtg_dict['govt_perf'] = dh_extract_9.loc[series_first_pid].get('Government Performance Rating')
            prnt_rtg_dict['imp_agcy_perf'] = dh_extract_9.loc[series_first_pid].get('Implementing Agency Performance Rating')
        else:
            print(f"Series First ProjectID {series_first_pid} not found in dh_extract_9")
            continue 
        
        
        # Compare current ProjectId's ratings with its parent and prepare output messages
        if pid_rtg_dict['outcome'] != prnt_rtg_dict['outcome']:
            output_results += 'Outcome '
            return_message += f"Outcome: Self = {pid_rtg_dict['outcome']} | Parent = {prnt_rtg_dict['outcome']}\n"
        if pid_rtg_dict['rel_obj'] != prnt_rtg_dict['rel_obj']:
            output_results += 'Relevance of Objective '
            return_message += f"Relevance of Objective: Self = {pid_rtg_dict['rel_obj']} | Parent = {prnt_rtg_dict['rel_obj']}\n"
        if pid_rtg_dict['rev_rel_obj'] != prnt_rtg_dict['rev_rel_obj']:
            output_results += 'Revised Relevance of Objective '
            return_message += f"Revised Relevance of Objective: Self = {pid_rtg_dict['rev_rel_obj']} | Parent = {prnt_rtg_dict['rev_rel_obj']}\n"
        if pid_rtg_dict['rel_design'] != prnt_rtg_dict['rel_design']:
            output_results += 'Relevance of Design '
            return_message += f"Relevance of Design: Self = {pid_rtg_dict['rel_design']} | Parent = {prnt_rtg_dict['rel_design']}\n"
        if pid_rtg_dict['rev_rel_design'] != prnt_rtg_dict['rev_rel_design']:
            output_results += 'Revised Relevance of Design '
            return_message += f"Revised Relevance of Design: Self = {pid_rtg_dict['rev_rel_design']} | Parent = {prnt_rtg_dict['rev_rel_design']}\n"
        if pid_rtg_dict['rel_prior_act'] != prnt_rtg_dict['rel_prior_act']:
            output_results += 'Relevance of Prior Action '
            return_message += f"Relevance of Prior Action: Self = {pid_rtg_dict['rel_prior_act']} | Parent = {prnt_rtg_dict['rel_prior_act']}\n"
        if pid_rtg_dict['rel_res_ind'] != prnt_rtg_dict['rel_res_ind']:
            output_results += 'Relevance of Results Indicators '
            return_message += f"Relevance of Results Indicators: Self = {pid_rtg_dict['rel_res_ind']} | Parent = {prnt_rtg_dict['rel_res_ind']}\n"
        if pid_rtg_dict['efficiency'] != prnt_rtg_dict['efficiency']:
            output_results += 'Efficiency '
            return_message += f"Efficiency: Self = {pid_rtg_dict['efficiency']} | Parent = {prnt_rtg_dict['efficiency']}\n"
        if pid_rtg_dict['rdo'] != prnt_rtg_dict['rdo']:
            output_results += 'RDO '
            return_message += f"RDO: Self = {pid_rtg_dict['rdo']} | Parent = {prnt_rtg_dict['rdo']}\n"
        if pid_rtg_dict['bank_perf'] != prnt_rtg_dict['bank_perf']:
            output_results += 'Bank Perf '
            return_message += f"Bank Perf: Self = {pid_rtg_dict['bank_perf']} | Parent = {prnt_rtg_dict['bank_perf']}\n"
        if pid_rtg_dict['qae'] != prnt_rtg_dict['qae']:
            output_results += 'QaE '
            return_message += f"QaE: Self = {pid_rtg_dict['qae']} | Parent = {prnt_rtg_dict['qae']}\n"
        if pid_rtg_dict['qos'] != prnt_rtg_dict['qos']:
            output_results += 'QoS '
            return_message += f"QoS: Self = {pid_rtg_dict['qos']} | Parent = {prnt_rtg_dict['qos']}\n"
        if pid_rtg_dict['borr_perf'] != prnt_rtg_dict['borr_perf']:
            output_results += 'Borrower Perf '
            return_message += f"Borrower Perf: Self = {pid_rtg_dict['borr_perf']} | Parent = {prnt_rtg_dict['borr_perf']}\n"
        if pid_rtg_dict['govt_perf'] != prnt_rtg_dict['govt_perf']:
            output_results += 'Govt Perf '
            return_message += f"Govt Perf: Self = {pid_rtg_dict['govt_perf']} | Parent = {prnt_rtg_dict['govt_perf']}\n"
        if pid_rtg_dict['imp_agcy_perf'] != prnt_rtg_dict['imp_agcy_perf']:
            output_results += 'Imp Agcy Perf '
            return_message += f"Imp Agency Perf: Self = {pid_rtg_dict['imp_agcy_perf']} | Parent = {prnt_rtg_dict['imp_agcy_perf']}\n"
        if pid_rtg_dict['me_qty'] != prnt_rtg_dict['me_qty']:
            output_results += 'M&E Quality '
            return_message += f"M&E Qty: Self = {pid_rtg_dict['me_qty']} | Parent = {prnt_rtg_dict['me_qty']}\n"
        if pid_rtg_dict['icr_qty'] != prnt_rtg_dict['icr_qty']:
            output_results += 'ICR Quality '
            return_message += f"ICR Qty: Self = {pid_rtg_dict['icr_qty']} | Parent = {prnt_rtg_dict['icr_qty']}\n"

        # Handling for different member types ('Intermediate', 'Last')
        if member_type == 'Intermediate':
            pass
        elif member_type == 'Last':
            pass

        if return_message == '':
            output_results = 'OK'
            return_message += f"Same as Parent ProjectID {series_first_pid}"

        # Finalize the output row for current ProjectId
        output_row.loc[0] = [pid, output_results, member_type, series_first_pid, pid_rtg_dict['outcome'], prnt_rtg_dict['outcome'], pid_rtg_dict['rel_obj'], prnt_rtg_dict['rel_obj'], pid_rtg_dict['rev_rel_obj'], prnt_rtg_dict['rev_rel_obj'], pid_rtg_dict['rel_design'], prnt_rtg_dict['rel_design'], pid_rtg_dict['rev_rel_design'], prnt_rtg_dict['rev_rel_design'], pid_rtg_dict['rel_prior_act'], prnt_rtg_dict['rel_prior_act'], pid_rtg_dict['rel_res_ind'], prnt_rtg_dict['rel_res_ind'], pid_rtg_dict['efficiency'], prnt_rtg_dict['efficiency'], pid_rtg_dict['rdo'], prnt_rtg_dict['rdo'], pid_rtg_dict['bank_perf'], prnt_rtg_dict['bank_perf'], pid_rtg_dict['qae'], prnt_rtg_dict['qae'], pid_rtg_dict['qos'], prnt_rtg_dict['qos'], pid_rtg_dict['borr_perf'], prnt_rtg_dict['borr_perf'], pid_rtg_dict['govt_perf'], prnt_rtg_dict['govt_perf'], pid_rtg_dict['imp_agcy_perf'], prnt_rtg_dict['imp_agcy_perf'], pid_rtg_dict['me_qty'], prnt_rtg_dict['me_qty'], pid_rtg_dict['icr_qty'], prnt_rtg_dict['icr_qty']]

    # Append the current output row to the main output DataFrame
    output = ps.concat([output, output_row], ignore_index=True)

    print(return_message)

# Set ProjectID as the index for the output DataFrame
output.set_index(index_col, inplace=True, verify_integrity=True)

#Export Output DataFrame to Excel
#output_filename = f"output_efficacy_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
#output.to_excel(output_filename)
output_filename = f"output_DPFSeries_{datetime.now().strftime('1')}.csv"
output.to_csv(output_filename)
print(output)

# COMMAND ----------

