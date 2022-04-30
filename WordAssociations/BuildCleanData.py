#!/usr/bin/env python

import pandas as pd
from lib.utils import read_qualtrics
from lib.clean import clean_responses, flag_misspelled

d = read_qualtrics('data/Word-Associations_MTurk.csv', melt = True)
exceptions = pd.read_csv('data/exceptions.csv')

z = exceptions['AssignmentStatus'] == 'Approved'
exceptions = exceptions.loc[z,:]
for i, row in exceptions.iterrows():
    z = d.loc[:,'WorkerId'] == row['WorkerId']
    z = z & d.loc[:,'HITId'] == row['HITId']
    z = z & d.loc[:,'AssignmentId'] == row['AssignmentId']
    d.loc[z,'AssignmentStatus'] = row['AssignmentStatus']

z = d.loc[:,'AssignmentStatus'] == 'Approved'
d = d.loc[z,:]

#d.to_csv('data/approved_responses.csv',index=False)

r = d.loc[:,('CUE','R1','R2','R3')]
r = pd.melt(r, id_vars='CUE', value_vars = ('R1','R2','R3'), var_name = 'RESP_ORDER', value_name = 'RESPONSE')
r['RESPONSE'] = clean_responses(r.loc[:,'RESPONSE'])

r.loc[:,'COUNT'] = 1
x = r.groupby(by=['CUE','RESP_ORDER','RESPONSE']).count()
x.to_csv('data/responses_by_cue_ordered.csv')
r = r.drop(columns=['COUNT'])

r = d.loc[:,('CUE','R1','R2','R3')]
r = pd.melt(r, id_vars='CUE', value_vars = ('R1','R2','R3'), var_name = 'RESP_ORDER', value_name = 'RESPONSE')
r['RESPONSE'] = clean_responses(r.loc[:,'RESPONSE'])
x = r.groupby(by=['CUE','RESPONSE']).count().rename(columns = {'RESP_ORDER': 'COUNT'})
x.to_csv('data/responses_by_cue.csv')

x['N_CUES'] = 1
x = x.groupby(['RESPONSE']).agg({'COUNT':'sum','N_CUES':'count'})
x.reset_index(inplace=True)
x['N_WORDS'] = [len(s.split()) for s in x['RESPONSE']]
x.loc[:,'UNKNOWN'] = flag_misspelled(x.reset_index()['RESPONSE'])
x.to_csv('data/unique_responses.csv', index = False)
