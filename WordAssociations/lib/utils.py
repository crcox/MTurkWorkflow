import pandas as pd
import numpy as np
import glob
import json
import os.path

def select_responses(d):
    d.columns = d.columns.droplevel(level=-1).droplevel(level=-1)
    a = list(d.columns).index('1_A1_4')
    b = list(d.columns).index('35_Q118_6') + 1
    d = pd.concat([
        d.loc[:,('MTURK_ID','HIT_ID','ASSIGNMENT_ID','LIST_ID')],
        d.iloc[:,a:b]] ,axis=1)
    return d

def select_metadata(d):
    d.columns = d.columns.droplevel(level=-1).droplevel(level=-1)
    metacol = ['MTURK_ID','HIT_ID','ASSIGNMENT_ID','LIST_ID',
               'Duration (in seconds)', 'RecordedDate', 'ResponseId',
               'LocationLatitude', 'LocationLongitude', 'DistributionChannel',
               'UserLanguage', 'DOB', 'EduLevel', 'Gender', 'IncomeLevel',
               'Ethnicity', 'Parent', 'Interact', 'Interact_Freq', 'Feedback']
    M = d.loc[:,metacol]

    EduLevel = [
        "Less than high school degree",
        "High school graduate",
        "Some college but no degree",
        "Associate degree in college (2-year)",
        "Bachelor's degree in college (4-year)",
        "Master's degree",
        "Doctoral degree",
        "Professional degree (JD,MD)" ]
    Gender = [
        "Male",
        "Female",
        "Other",
        "Would rather not say" ]
    IncomeLevel = [
        "Less than $20,000",
        "$20,001--$40,000",
        "$40,001--$75,000",
        "$75,001--$150,000",
        "Above $150,000" ]
    Race = [
        "White/Caucasian",
        "African-American",
        "Asian",
        "Native American",
        "Pacific Islander",
        "Other",
        "Would rather not say" ]
    Ethnicity = [
        "Hispanic",
        "non-Hispanic",
        "",
        "Would rather not say" ]
    Parent = [""]*31 + [
        "Yes",
        "No" ]
    Interact = [""]*22 + [
        "Yes",
        "No" ]
    Interact_Freq = [""]*10 + [
        "Daily",
        "A few times a week",
        "Once a week",
        "Once a month",
        "Rarely" ]

    float_to_int = ['EduLevel','Gender','IncomeLevel','Ethnicity','Parent',
                    'Interact','Interact_Freq']
    for x in float_to_int:
        M.loc[:,x] = M[x].astype('Int64')-1

    M.loc[:,'EduLevel'] = [np.NaN if pd.isnull(i) else EduLevel[i] for i in M['EduLevel']]
    M.loc[:,'Gender'] = [np.NaN if pd.isnull(i) else Gender[i] for i in M['Gender']]
    M.loc[:,'IncomeLevel'] = [np.NaN if pd.isnull(i) else IncomeLevel[i] for i in M['IncomeLevel']]
    M.loc[:,'Ethnicity'] = [np.NaN if pd.isnull(i) else Ethnicity[i] for i in M['Ethnicity']]
    M.loc[:,'Parent'] = [np.NaN if pd.isnull(i) else Parent[i] for i in M['Parent']]
    M.loc[:,'Interact'] = [np.NaN if pd.isnull(i) else Interact[i] for i in M['Interact']]
    M.loc[:,'Interact_Freq'] = [np.NaN if pd.isnull(i) else Interact_Freq[i] for i in M['Interact_Freq']]

    tmp = []
    for index,row in d.loc[:,['Race_1','Race_2','Race_4','Race_5','Race_6','Race_7','Race_8','Race_7_TEXT']].iterrows():
        r = list(Race)
        check = row.loc[['Race_1','Race_2','Race_4','Race_5','Race_6']]
        if not pd.isnull(row['Race_7']):
            # If "Other" was selected ...
            if pd.isnull(row['Race_7_TEXT']) and not np.any(pd.isnull(check)):
                # If they don't fill in the box AND have indicated no other races ...
                r[5] = "Would rather not say"
            elif not pd.isnull(row['Race_7_TEXT']):
                # If they do fill in the box ...
                r[5] = row['Race_7_TEXT']

        if np.all(pd.isnull(row)):
            # If they fill in absolutely nothing ...
            tmp.append("Would rather not say")
        else:
            x = [r[i] for i in range(len(row)-1) if not pd.isnull(row[i])]
            tmp.append(','.join(x))

        if M.loc[index,"Gender"] == "Other":
            M.loc[index,"Gender"] = d.loc[index,"Gender_3_TEXT"]

    M.loc[:,'Race'] = tmp
    return M

def melt_responses(d, id_vars):
    d = pd.melt(d,
                id_vars=id_vars,
                var_name = 'CUE_CODE',
                value_name = 'RESPONSE')
    z = ~d['RESPONSE'].isnull()
    d = d.loc[z,:]
    d = d.reset_index()

    x = pd.DataFrame(
            data = list(d['CUE_CODE'].str.split('_')),
            columns = ('CUE_ID','LIST_ID','RESP_ID'))
    d = d.drop(labels = 'CUE_CODE', axis = 1)
    d = pd.concat([x,d], axis = 1)

    d = d.set_index(keys=id_vars + ['LIST_ID','CUE_ID','RESP_ID'])
    d = d.unstack(level=-1)
    d = d.reset_index(id_vars + ['LIST_ID','CUE_ID'])
    d.columns = ['_'.join(col).strip('_') for col in d.columns.values]
    d = d.drop(labels = ['index_4','index_5','index_6'], axis = 1)
    d.loc[:,'CUE_ID'] = d['CUE_ID'].astype(np.int64)
    d = d.rename(columns = {
        'RESPONSE_4':'R1',
        'RESPONSE_5':'R2',
        'RESPONSE_6':'R3'}
    )
    return d

def read_hits():
    hitfiles = glob.glob(os.path.join('data','HITS','*.json'))
    h = []
    for hf in hitfiles:
        with open(hf,'rb') as f:
            h.extend(json.load(f)['Assignments'])

    HITs = pd.DataFrame(h).loc[:,('AssignmentId','AssignmentStatus','HITId','WorkerId')]
    return HITs

def read_qualtrics(filename, melt = False, meta = False):
    HITs = read_hits()
    d = pd.read_csv(filename, header = [0,1,2], low_memory = False)
    if meta:
        d = select_metadata(d)
    else:
        d = select_responses(d)
    d = d.rename(columns={
        'MTURK_ID'     :'WorkerId',
        'HIT_ID'       :'HITId',
        'ASSIGNMENT_ID':'AssignmentId',
        'LIST_ID'      :'ListId'})
    # This selects only the "Submitted" HITs (not Approved or Rejected)
    d = d.merge(HITs, how='left')
    if melt:
        d = melt_responses(d, id_vars=[
            'WorkerId',
            'HITId',
            'AssignmentId',
            'ListId',
            'AssignmentStatus'])
        stim = pd.read_csv("stimuli/OrderB.csv").rename(columns={"LIST_ID": "ListId"})
        d = d.merge(stim, how='left')

    return d
