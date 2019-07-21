import pandas as pd
import numpy as np

def select_responses(d):
    d.columns = d.columns.droplevel(level=-1).droplevel(level=-1)
    a = list(d.columns).index('1_A1_4')
    b = list(d.columns).index('35_Q118_6') + 1
    d = pd.concat([
        d.loc[:,('MTURK_ID','HIT_ID','ASSIGNMENT_ID','LIST_ID')],
        d.iloc[:,a:b]] ,axis=1)
    return d

def melt_responses(d, id_vars):
    d = pd.melt(d,
                id_vars=id_vars,
                var_name = "CUE_CODE",
                value_name = "RESPONSE")
    z = ~d['RESPONSE'].isnull()
    d = d.loc[z,:]
    d = d.reset_index()

    x = pd.DataFrame(
            data = list(d['CUE_CODE'].str.split('_')),
            columns = ("CUE_ID","LIST_ID","RESP_ID"))
    d = d.drop(labels = 'CUE_CODE', axis = 1)
    d = pd.concat([x,d], axis = 1)

    d = d.set_index(keys=id_vars + ["LIST_ID","CUE_ID","RESP_ID"])
    d = d.unstack(level=-1)
    d = d.reset_index(id_vars + ["LIST_ID","CUE_ID"])
    d.columns = ['_'.join(col).strip('_') for col in d.columns.values]
    d = d.drop(labels = ['index_4','index_5','index_6'], axis = 1)
    d.loc[:,'CUE_ID'] = d['CUE_ID'].astype(np.int64)
    d = d.rename(columns = {
        'RESPONSE_4':'R1',
        'RESPONSE_5':'R2',
        'RESPONSE_6':'R3'}
    )
    return d
