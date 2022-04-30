#!/usr/bin/env python

import pandas as pd
import json
import glob
import os.path

hits = glob.glob(os.path.join("data","HITS","*.json"))
hits_definition = [os.path.join("data","HITS","definition",os.path.basename(x)) for x in hits]

DD = []
HH = []
for h,d in zip(hits,hits_definition):
    with open(h, 'rb') as fh, open(d, 'rb') as fd:
        H = json.load(fh)['Assignments']
        HH.extend(H)

        D = json.load(fd)['HIT']
        keys = [
            'HITId',
            'HITTypeId',
            'Title',
            'Keywords',
            'Reward',
            'CreationTime',
            'MaxAssignments',
            'AssignmentDurationInSeconds',
            'AutoApprovalDelayInSeconds',
            'Expiration'
        ]
        DD.append({k: D[k] for k in keys})

D = pd.DataFrame.from_dict(DD)
H = pd.DataFrame.from_dict(HH)
H = H.merge(D, how = 'left', on = 'HITId')
H = H.drop(columns = ['Answer'])
H.to_csv("Batch_Report.csv", index = False)
