# Databricks notebook source

# Import Libraries
from datetime import datetime
import pandas as pd

# Load DataHub Extract into DataFrame (to be replaced with a direct connection to the DataLake)
dh_extract = pd.read_excel('IEG Data Hub - IEG Ratings.xlsx', sheet_name='Export',
                           usecols=['Project ID', 'Exit FY', 'Instrument Type Name', 'Evaluation Date', 'Evaluation Type',
                                    'Outcome Rating', 'Quality At Entry Rating', 'Quality At Supervision Rating',
                                    'Overall Bank Performance Rating', 'Overall Borrower Performance Rating',
                                    'ME Quality Rating', 'Latest Evaluation Flag', 'Latest ICRR Flag', 'Latest PPAR Flag'],
                           dtype=str)

# Load Data Explorer Extract into DataFrame (to be replaced with a direct connection to the API)
ecd_extract = pd.read_excel('Data Explorer.xlsx', sheet_name='Sheet 1', dtype=str)

# Merge DataHub and Data Explorer extracts on common indices
merged_data = pd.merge(dh_extract, ecd_extract, how='outer', left_on=['Project ID', 'Evaluation Date', 'Evaluation Type'],
                       right_on=['PROJ_ID', 'EVAL_DATE', 'EVAL_TYPE_CODE'])

# Create Output Report DataFrame
output_cols = ['Project ID', 'Eval Date', 'Eval Type', 'Latest Eval', 'Latest ICRR', 'Latest PPAR', 'Test Results', 'Inst Type', 'Exit FY ECD', 'Exit FY DH', 'Outcome ECD', 'Outcome DH', 'Bank Perf ECD', 'Bank Perf DH', 'QaE ECD', 'QaE DH', 'QoS ECD', 'QoS DH', 'Borr Perf ECD', 'Borr Perf DH', 'ME Qty ECD', 'ME Qty DH']
output = pd.DataFrame(columns=output_cols)

# Check fields to map cases with empty and "not rated" values
def check_val(txt):
    txt_str = str(txt).casefold()
    if txt_str == '0':
        return ''
    elif txt_str in ['not applicable', 'not applicable/not related', 'not available', 'non-evaluable', 'not rated']:
        return ''
    else:
        return txt_str

for row in dh_extract.index:
    # Initialize dictionaries and variables for individual evaluation analysis
    dh_inst_type = ''
    dh_exit_fy = ''
    ecd_exit_fy = ''
    dh_rtg_dict = {'outcome':'', 'bank_perf':'', 'qae':'', 'qos':'', 'borr_perf':'', 'me_qty':''}
    ecd_rtg_dict = {'outcome':'', 'bank_perf':'', 'qae':'', 'qos':'', 'borr_perf':'', 'me_qty':''}
    dh_latest_eval = ''
    dh_latest_icrr = ''
    dh_latest_ppar = ''

    return_message = ''
    output_results = 'Check: '
    
    print(f"\nEvaluation: {row}")
    print('------------------')

    # Check if evaluation is in Data Explorer
    if not (row in ecd_extract.index):
        output_results += 'Eval not found in Data Explorer'
        return_message += f"{output_results}\n"
    else:        
        # Get DataHub data
        inst_type = dh_extract.loc[row].get('Instrument Type Name')
        dh_exit_fy = dh_extract.loc[row].get('Exit FY')
        dh_rtg_dict['outcome'] = dh_extract.loc[row].get('Outcome Rating')
        dh_rtg_dict['bank_perf'] = dh_extract.loc[row].get('Overall Bank Performance Rating')
        dh_rtg_dict['qae'] = dh_extract.loc[row].get('Quality At Entry Rating')
        dh_rtg_dict['qos'] = dh_extract.loc[row].get('Quality At Supervision Rating')
        dh_rtg_dict['borr_perf'] = dh_extract.loc[row].get('Overall Borrower Performance Rating')
        dh_rtg_dict['me_qty'] = dh_extract.loc[row].get('ME Quality Rating')
        dh_latest_eval = dh_extract.loc[row].get('Latest Evaluation Flag')
        dh_latest_icrr = dh_extract.loc[row].get('Latest ICRR Flag')
        dh_latest_ppar = dh_extract.loc[row].get('Latest PPAR Flag')

        # Get Data Explorer data
        ecd_exit_fy = ecd_extract.loc[row].get('EXIT_FY')
        ecd_rtg_dict['outcome'] = ecd_extract.loc[row].get('OUTCOME_DESC')
        ecd_rtg_dict['bank_perf'] = ecd_extract.loc[row].get('OVERALL_BANK_PERF_DESC')
        ecd_rtg_dict['qae'] = ecd_extract.loc[row].get('BANK_QLTY_AT_ENTRY_DESC')
        ecd_rtg_dict['qos'] = ecd_extract.loc[row].get('BANK_QLTY_OF_SUPV_DESC')
        ecd_rtg_dict['borr_perf'] = ecd_extract.loc[row].get('OVERALL_BORR_PERF_DESC')
        ecd_rtg_dict['me_qty'] = ecd_extract.loc[row].get('ME_QLTY_DESC')

        # Compare IEG Ratings from Data Explorer with DataHub
        if check_val(ecd_exit_fy) != check_val(dh_exit_fy):
            output_results += 'Exit FY '
            return_message += f"Exit FY: ECD = {ecd_exit_fy} | DH = {dh_exit_fy}\n"
        if check_val(ecd_rtg_dict['outcome']) != check_val(dh_rtg_dict['outcome']):
            output_results += 'Outcome '
            return_message += f"Outcome: ECD = {ecd_rtg_dict['outcome']} | DH = {dh_rtg_dict['outcome']}\n"
        if check_val(ecd_rtg_dict['bank_perf']) != check_val(dh_rtg_dict['bank_perf']):
            output_results += 'Bank Perf '
            return_message += f"Bank Perf: ECD = {ecd_rtg_dict['bank_perf']} | DH = {dh_rtg_dict['bank_perf']}\n"
        if check_val(ecd_rtg_dict['qae']) != check_val(dh_rtg_dict['qae']):
            output_results += 'QaE '
            return_message += f"QaE: ECD = {ecd_rtg_dict['qae']} | DH = {dh_rtg_dict['qae']}\n"
        if check_val(ecd_rtg_dict['qos']) != check_val(dh_rtg_dict['qos']):
            output_results += 'QoS '
            return_message += f"QoS: ECD = {ecd_rtg_dict['qos']} | DH = {dh_rtg_dict['qos']}\n"
        if check_val(ecd_rtg_dict['borr_perf']) != check_val(dh_rtg_dict['borr_perf']):
            output_results += 'Borrower Perf '
            return_message += f"Borrower Perf: ECD = {ecd_rtg_dict['bank_perf']} | DH = {dh_rtg_dict['borr_perf']}\n"
        if check_val(ecd_rtg_dict['me_qty']) != check_val(dh_rtg_dict['me_qty']):
            output_results += 'M&E Quality '
            return_message += f"M&E Qty: ECD = {ecd_rtg_dict['me_qty']} | DH = {dh_rtg_dict['me_qty']}\n"

    if return_message == '':
        output_results = 'OK'
        return_message += 'No differences\n'
    else:
        output_results = 'Check: ' + output_results  # Added to include 'Check: ' in the output

    # Append Row DataFrame to Output DataFrame
    output_row = pd.DataFrame([[dh_extract.iloc[row]['Project ID'], dh_extract.iloc[row]['Evaluation Date'], dh_extract.iloc[row]['Evaluation Type'], dh_latest_eval, dh_latest_icrr, dh_latest_ppar, output_results, inst_type, ecd_exit_fy, dh_exit_fy, ecd_rtg_dict['outcome'], dh_rtg_dict['outcome'], ecd_rtg_dict['bank_perf'], dh_rtg_dict['bank_perf'], ecd_rtg_dict['qae'], dh_rtg_dict['qae'], ecd_rtg_dict['qos'], dh_rtg_dict['qos'], ecd_rtg_dict['borr_perf'], dh_rtg_dict['borr_perf'], ecd_rtg_dict['me_qty'], dh_rtg_dict['me_qty']]], columns=output_cols)
    output = pd.concat([output, output_row], ignore_index=True)

# Set Output DataFrame Index
output.set_index(['Project ID', 'Eval Date', 'Eval Type'], inplace=True, verify_integrity=True)

# Export Output DataFrame to CSV
output_filename = f"V2_output_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
output.to_csv(output_filename)
print(output)

# COMMAND ----------



# COMMAND ----------

