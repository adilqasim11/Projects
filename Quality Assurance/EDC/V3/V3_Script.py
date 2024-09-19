# Databricks notebook source
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import Libraries
import pandas as pd
import datetime

# Load List of ProjectIds from ICRR System
sheet_name = 'Sheet1'
index_col = 'Project Id'
with pd.ExcelFile('IEG Data Hub -ICRR Ratings.xlsx') as xlsx: icrr_system_source = pd.read_excel(xlsx, sheet_name=sheet_name, skiprows=2, index_col=index_col)
pid_list = icrr_system_source.index
#pid_list = ['P120860', 'P126325', 'P163968', 'P012345', 'P096019', 'P099709']

# Load Data Explorer Extract into DataFrame (to be replaced with a direct connection to the API)
sheet_name = 'Sheet 1'
index_col = 'PROJ_ID'
with pd.ExcelFile('PROJECT_IEG_RATING.xlsx') as xlsx: ecd_extract = pd.read_excel(xlsx, sheet_name=sheet_name, index_col=index_col, skiprows=4, keep_default_na=False, dtype=str)

print(icrr_system_source.columns)

# Load DataHub Extract Tabs into DataFrame (to be replaced with a direct connection to the DataLake)
sheet_name = 'Export'
index_col = 'Project Id'
with pd.ExcelFile('1a.xlsx') as xlsx: dh_extract_1a = pd.read_excel(xlsx, sheet_name=sheet_name, index_col=index_col, keep_default_na=False, dtype=str)
with pd.ExcelFile('3a.xlsx') as xlsx: dh_extract_3a = pd.read_excel(xlsx, sheet_name=sheet_name, index_col=index_col, keep_default_na=False, dtype=str)
with pd.ExcelFile('5.xlsx') as xlsx: dh_extract_5 = pd.read_excel(xlsx, sheet_name=sheet_name, index_col=index_col, keep_default_na=False, dtype=str)
with pd.ExcelFile('8.xlsx') as xlsx: dh_extract_8 = pd.read_excel(xlsx, sheet_name=sheet_name, index_col=index_col, keep_default_na=False, dtype=str)
with pd.ExcelFile('9.xlsx') as xlsx: dh_extract_9 = pd.read_excel(xlsx, sheet_name=sheet_name, index_col=index_col, keep_default_na=False, dtype=str)
with pd.ExcelFile('12.xlsx') as xlsx: dh_extract_12 = pd.read_excel(xlsx, sheet_name=sheet_name, index_col=index_col, keep_default_na=False, dtype=str)

output_cols = ['ProjectID', 'Test Results', 'Inst Type', 'Outcome ECD', 'Outcome DH', 'Rel Obj ECD', 'Rel Obj DH', 'Rel Design ECD', 'Rel Design DH', 'Efficiency ECD', 'Efficiency DH', 'RDO ECD', 'RDO DH', 'Bank Perf ECD', 'Bank Perf DH', 'QaE ECD', 'QaE DH', 'QoS ECD', 'QoS DH', 'Borr Perf ECD', 'Borr Perf DH', 'Imp Agcy Perf ECD', 'Imp Agcy Perf DH', 'Borr Comp ECD', 'Borr Comp DH', 'ICR Qty ECD', 'ICR Qty DH']
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

for pid in pid_list:
    # Initialize dictionaries and variables for individual evaluation analysis
    dh_inst_type = ''
    ecd_rtg_dict = {'outcome':'', 'rel_obj':'', 'rel_design':'', 'efficiency':'', 'rdo':'', 'bank_perf':'', 'qae':'', 'qos':'', 'borr_perf':'', 'imp_agcy_perf':'', 'borr_comp':'', 'icr_qty':''}
    dh_rtg_dict = {'outcome':'', 'rel_obj':'', 'rel_design':'', 'efficiency':'', 'rdo':'', 'bank_perf':'', 'qae':'', 'qos':'', 'borr_perf':'', 'imp_agcy_perf':'', 'borr_comp':'', 'icr_qty':''}
    return_message = ''
    output_results = 'Check: '
    
    print(f"\nProjectID: {pid}")
    print('------------------')
    
    # Check if ProjectId is in Data Explorer
    if pid not in ecd_extract.index:
        print(f"ProjectId {pid} not found in Data Explorer")
        continue
    
    # Check if ProjectId is in DataHub
    if pid not in dh_extract_1a.index:
        print(f"ProjectId {pid} not found in DataHub")
        continue

    # Get DataHub data from Extract Tabs
    inst_type = dh_extract_1a.loc[pid].get('Instrument Type Name')
    dh_rtg_dict['outcome'] = dh_extract_12.loc[pid].get('Outcome Rating')
    dh_rtg_dict['rel_obj'] = dh_extract_3a.loc[pid].get('Relevance Of Objective Rating')
    dh_rtg_dict['rel_design'] = dh_extract_3a.loc[pid].get('Relevance Of Design Rating')
    dh_rtg_dict['efficiency'] = dh_extract_5.loc[pid].get('Efficiency Rating')
    dh_rtg_dict['rdo'] = dh_extract_12.loc[pid].get('Risk To Development Outcome Rating')
    dh_rtg_dict['bank_perf'] = dh_extract_12.loc[pid].get('Overall Bank Performance Rating')
    dh_rtg_dict['qae'] = dh_extract_8.loc[pid].get('Quality At Entry Rating')
    dh_rtg_dict['qos'] = dh_extract_8.loc[pid].get('Quality At Supervision Rating')
    dh_rtg_dict['borr_perf'] = dh_extract_12.loc[pid].get('Overall Borrower Performance Rating')
    dh_rtg_dict['imp_agcy_perf'] = dh_extract_9.loc[pid].get('Implementing Agency Performance Rating')
    dh_rtg_dict['borr_comp'] = dh_extract_9.loc[pid].get('Borrower Compliance Rating')
    dh_rtg_dict['icr_qty'] = dh_extract_12.loc[pid].get('ICR Quality Rating')

    
    # Get Data Explorer data for each column
    # Outcome ECD
    outcome_ecd_data = ecd_extract.loc[pid].get('IEG_OUTCOME_RTG_NAME')
    if isinstance(outcome_ecd_data, str):
        ecd_rtg_dict['outcome'] = outcome_ecd_data
    else:
        try:
            if not outcome_ecd_data.empty:
                ecd_rtg_dict['outcome'] = outcome_ecd_data.iloc[0]
            else:
                ecd_rtg_dict['outcome'] = ''
        except AttributeError:
            ecd_rtg_dict['outcome'] = ''

    # Relevant Objectives ECD
    rel_obj_ecd_data = ecd_extract.loc[pid].get('IEG_RELEVANT_OBJECTIVES_RTG_NAME')
    if isinstance(rel_obj_ecd_data, str):
        ecd_rtg_dict['rel_obj'] = rel_obj_ecd_data
    else:
        try:
            if not rel_obj_ecd_data.empty:
                ecd_rtg_dict['rel_obj'] = rel_obj_ecd_data.iloc[0]
            else:
                ecd_rtg_dict['rel_obj'] = ''
        except AttributeError:
            ecd_rtg_dict['rel_obj'] = ''

    # Rel Design ECD
    rel_design_ecd_data = ecd_extract.loc[pid].get('IEG_RELEVANT_DESIGN_RTG_NAME')
    if isinstance(rel_design_ecd_data, str):
        ecd_rtg_dict['rel_design'] = rel_design_ecd_data
    else:
        try:
            if not rel_design_ecd_data.empty:
                ecd_rtg_dict['rel_design'] = rel_design_ecd_data.iloc[0]
            else:
                ecd_rtg_dict['rel_design'] = ''
        except AttributeError:
            ecd_rtg_dict['rel_design'] = ''

    # Efficiency ECD
    efficiency_ecd_data = ecd_extract.loc[pid].get('IEG_EFFICIENCY_RTG_NAME')
    if isinstance(efficiency_ecd_data, str):
        ecd_rtg_dict['efficiency'] = efficiency_ecd_data
    else:
        try:
            if not efficiency_ecd_data.empty:
                ecd_rtg_dict['efficiency'] = efficiency_ecd_data.iloc[0]
            else:
                ecd_rtg_dict['efficiency'] = ''
        except AttributeError:
            ecd_rtg_dict['efficiency'] = ''

    # RDO ECD
    rdo_ecd_data = ecd_extract.loc[pid].get('IEG_RISK_TO_DEV_OUTCOME_NAME')
    if isinstance(rdo_ecd_data, str):
        ecd_rtg_dict['rdo'] = rdo_ecd_data
    else:
        try:
            if not rdo_ecd_data.empty:
                ecd_rtg_dict['rdo'] = rdo_ecd_data.iloc[0]
            else:
                ecd_rtg_dict['rdo'] = ''
        except AttributeError:
            ecd_rtg_dict['rdo'] = ''

    # Bank Perf ECD
    bank_perf_ecd_data = ecd_extract.loc[pid].get('IEG_OVERALL_BANK_PERF_NAME')
    if isinstance(bank_perf_ecd_data, str):
        ecd_rtg_dict['bank_perf'] = bank_perf_ecd_data
    else:
        try:
            if not bank_perf_ecd_data.empty:
                ecd_rtg_dict['bank_perf'] = bank_perf_ecd_data.iloc[0]
            else:
                ecd_rtg_dict['bank_perf'] = ''
        except AttributeError:
            ecd_rtg_dict['bank_perf'] = ''

    # QaE ECD
    qae_ecd_data = ecd_extract.loc[pid].get('IEG_QLTY_AT_ENTRY_RTG_NAME')
    if isinstance(qae_ecd_data, str):
        ecd_rtg_dict['qae'] = qae_ecd_data
    else:
        try:
            if not qae_ecd_data.empty:
                ecd_rtg_dict['qae'] = qae_ecd_data.iloc[0]
            else:
                ecd_rtg_dict['qae'] = ''
        except AttributeError:
            ecd_rtg_dict['qae'] = ''

    # QoS ECD
    qos_ecd_data = ecd_extract.loc[pid].get('IEG_SUPV_RTG_NAME')
    if isinstance(qos_ecd_data, str):
        ecd_rtg_dict['qos'] = qos_ecd_data
    else:
        try:
            if not qos_ecd_data.empty:
                ecd_rtg_dict['qos'] = qos_ecd_data.iloc[0]
            else:
                ecd_rtg_dict['qos'] = ''
        except AttributeError:
            ecd_rtg_dict['qos'] = ''

    # Borr Perf ECD
    borr_perf_ecd_data = ecd_extract.loc[pid].get('IEG_OVERALL_BORWR_PERF_RTG_NAME')
    if isinstance(borr_perf_ecd_data, str):
        ecd_rtg_dict['borr_perf'] = borr_perf_ecd_data
    else:
        try:
            if not borr_perf_ecd_data.empty:
                ecd_rtg_dict['borr_perf'] = borr_perf_ecd_data.iloc[0]
            else:
                ecd_rtg_dict['borr_perf'] = ''
        except AttributeError:
            ecd_rtg_dict['borr_perf'] = ''

    # Imp Agcy Perf ECD
    imp_agcy_perf_ecd_data = ecd_extract.loc[pid].get('IEG_BORWR_IMPLTN_RTG_NAME')
    if isinstance(imp_agcy_perf_ecd_data, str):
        ecd_rtg_dict['imp_agcy_perf'] = imp_agcy_perf_ecd_data
    else:
        try:
            if not imp_agcy_perf_ecd_data.empty:
                ecd_rtg_dict['imp_agcy_perf'] = imp_agcy_perf_ecd_data.iloc[0]
            else:
                ecd_rtg_dict['imp_agcy_perf'] = ''
        except AttributeError:
            ecd_rtg_dict['imp_agcy_perf'] = ''

    # Borr Comp ECD
    borr_comp_ecd_data = ecd_extract.loc[pid].get('IEG_BORWR_CMPLNC_RTG_NAME')
    if isinstance(borr_comp_ecd_data, str):
        ecd_rtg_dict['borr_comp'] = borr_comp_ecd_data
    else:
        try:
            if not borr_comp_ecd_data.empty:
                ecd_rtg_dict['borr_comp'] = borr_comp_ecd_data.iloc[0]
            else:
                ecd_rtg_dict['borr_comp'] = ''
        except AttributeError:
            ecd_rtg_dict['borr_comp'] = ''

    # ICR Qty ECD
    icr_qty_ecd_data = ecd_extract.loc[pid].get('IEG_ICR_QLTY_RTG_NAME')
    if isinstance(icr_qty_ecd_data, str):
        ecd_rtg_dict['icr_qty'] = icr_qty_ecd_data
    else:
        try:
            if not icr_qty_ecd_data.empty:
                ecd_rtg_dict['icr_qty'] = icr_qty_ecd_data.iloc[0]
            else:
                ecd_rtg_dict['icr_qty'] = ''
        except AttributeError:
            ecd_rtg_dict['icr_qty'] = ''






    # Compare IEG Ratings from Data Explorer with DataHub
    if check_val(ecd_rtg_dict['outcome']) != check_val(dh_rtg_dict['outcome']):
        output_results += 'Outcome '
        return_message += f"Outcome: ECD = {ecd_rtg_dict['outcome']} | DH = {dh_rtg_dict['outcome']}\n"
    if check_val(ecd_rtg_dict['rel_obj']) != check_val(dh_rtg_dict['rel_obj']):
        output_results += 'Relevance of Objective '
        return_message += f"Relevance of Objective: ECD = {ecd_rtg_dict['rel_obj']} | DH = {dh_rtg_dict['rel_obj']}\n"
    if check_val(ecd_rtg_dict['rel_design']) != check_val(dh_rtg_dict['rel_design']):
        output_results += 'Relevance of Design '
        return_message += f"Relevance of Design: ECD = {ecd_rtg_dict['rel_design']} | DH = {dh_rtg_dict['rel_design']}\n"
    if check_val(ecd_rtg_dict['efficiency']) != check_val(dh_rtg_dict['efficiency']):
        output_results += 'Efficiency '
        return_message += f"Efficiency: ECD = {ecd_rtg_dict['efficiency']} | DH = {dh_rtg_dict['efficiency']}\n"
    if check_val(ecd_rtg_dict['rdo']) != check_val(dh_rtg_dict['rdo']):
        output_results += 'RDO '
        return_message += f"RDO: ECD = {ecd_rtg_dict['rdo']} | DH = {dh_rtg_dict['rdo']}\n"
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
        return_message += f"Borrower Perf: ECD = {ecd_rtg_dict['borr_perf']} | DH = {dh_rtg_dict['borr_perf']}\n"
    if check_val(ecd_rtg_dict['imp_agcy_perf']) != check_val(dh_rtg_dict['imp_agcy_perf']):
        output_results += 'Imp Agcy Perf '
        return_message += f"Imp Agency Perf: ECD = {ecd_rtg_dict['imp_agcy_perf']} | DH = {dh_rtg_dict['imp_agcy_perf']}\n"
    if check_val(ecd_rtg_dict['borr_comp']) != check_val(dh_rtg_dict['borr_comp']):
        output_results += 'Borrower Comp '
        return_message += f"Borrower Comp: ECD = {ecd_rtg_dict['borr_comp']} | DH = {dh_rtg_dict['borr_comp']}\n"
    if check_val(ecd_rtg_dict['icr_qty']) != check_val(dh_rtg_dict['icr_qty']):
        output_results += 'ICR Quality '
        return_message += f"ICR Qty: ECD = {ecd_rtg_dict['icr_qty']} | DH = {dh_rtg_dict['icr_qty']}\n"

    if return_message == '':
        output_results = 'OK'
        return_message += 'No differences\n'
    else:
        output_results = 'Check: ' + output_results  # Added to include 'Check: ' in the output

    # Append Row DataFrame to Output DataFrame
    output_row = pd.DataFrame(columns=output_cols)
    output_row.loc[0] = [pid, output_results, inst_type, ecd_rtg_dict['outcome'], dh_rtg_dict['outcome'], ecd_rtg_dict['rel_obj'], dh_rtg_dict['rel_obj'], ecd_rtg_dict['rel_design'], dh_rtg_dict['rel_design'], ecd_rtg_dict['efficiency'], dh_rtg_dict['efficiency'], ecd_rtg_dict['rdo'], dh_rtg_dict['rdo'], ecd_rtg_dict['bank_perf'], dh_rtg_dict['bank_perf'], ecd_rtg_dict['qae'], dh_rtg_dict['qae'], ecd_rtg_dict['qos'], dh_rtg_dict['qos'], ecd_rtg_dict['borr_perf'], dh_rtg_dict['borr_perf'], ecd_rtg_dict['imp_agcy_perf'], dh_rtg_dict['imp_agcy_perf'], ecd_rtg_dict['borr_comp'], dh_rtg_dict['borr_comp'], ecd_rtg_dict['icr_qty'], dh_rtg_dict['icr_qty']]

    output = pd.concat([output, output_row], ignore_index=True)

# Export Output DataFrame to CSV
output_filename = f"V3_Output_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
output.to_csv(output_filename, index=False)
#print(output)



# COMMAND ----------

