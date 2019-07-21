#!/usr/bin/env python

import pandas as pd
import numpy as np
import json
import glob
import os.path
from lib.utils import select_responses,melt_responses
import sys

with open("data/MTurk-Qualification-Key.json",'rb') as f:
    q = json.load(f)['QualificationTypes']

hitlist = pd.read_csv('summary/hits.csv')
hitlist = hitlist.loc[:,('HIT_ID','LIST_ID')]
#hitlist = hitlist.rename(columns={'HITId':'HIT_ID','ListId':'LIST_ID'})
hitlist = hitlist.rename(columns={'HIT_ID':'HITId','LIST_ID':'ListId'})
hitlist['Name'] = ["Word Associations {i:02d}".format(i=i) for i in hitlist['ListId']]

Qualifications = pd.DataFrame(q)
Qualifications = hitlist.merge(Qualifications, how='left')

hitfiles = glob.glob("data/HITS/*.json")
h = []
for hf in hitfiles:
    with open(hf,'rb') as f:
        h.extend(json.load(f)['Assignments'])

HITs = pd.DataFrame(h)
tmp = HITs.merge(hitlist, how='left')
print(HITs['AssignmentStatus'].value_counts())
print(pd.crosstab(tmp['AssignmentStatus'],tmp['ListId']))
z = HITs['AssignmentStatus'].values == "Submitted"
if not np.any(z):
    print("There are no new assignments to evaluate.")
    sys.exit(0)

HITs_new = HITs.loc[z,("AssignmentId","AssignmentStatus","HITId","WorkerId")]
d = HITs_new.merge(Qualifications, how='left')

x = []
if not os.path.exists('new-qualification-assignments'):
    os.mkdir('new-qualification-assignments')

for index,row in d.iterrows():
    fpath = os.path.join('new-qualification-assignments',"{:04d}_{:02d}.json".format(index,0))
    with open(fpath,'w') as f:
        json.dump({
            "QualificationTypeId": row['QualificationTypeId'],
            "WorkerId": row['WorkerId'],
            "IntegerValue": 1,
            "SendNotification": False}, f, indent=4, ensure_ascii=True)

    fpath = os.path.join('new-qualification-assignments',"{:04d}_{:02d}.json".format(index,1))
    with open(fpath,'w') as f:
        json.dump({
            "QualificationTypeId": '3QTDD8KTB60OW3CGXHY9CIQCFHQVHI', # Word Associations Any
            "WorkerId": row['WorkerId'],
            "IntegerValue": 1,
            "SendNotification": False}, f, indent=4, ensure_ascii=True)

print("* ====")
print("* New qualification assignments are staged in:")
print("* ./new-qualification-assignments/????_??.json")
print("*")
print("* To apply them, run:")
print("* ./SubmitQualificationAssignments.sh")
print("* ====")
print("")

d = d.loc[:,('AssignmentId', 'AssignmentStatus', 'HITId', 'WorkerId', 'ListId', 'Name', 'QualificationTypeId')]

q = pd.read_csv('data/Word-Associations_MTurk.csv',header=[0,1,2],low_memory=False)
q = select_responses(q)
q = q.rename(columns={
    'MTURK_ID'     :'WorkerId',
    'HIT_ID'       :'HITId',
    'ASSIGNMENT_ID':'AssignmentId',
    'LIST_ID'      :'ListId'})
# This selects only the "Submitted" HITs (not Approved or Rejected)
d = d.merge(q, how='left')
d = melt_responses(d, id_vars=[
    'WorkerId',
    'HITId',
    'AssignmentId',
    'ListId',
    'AssignmentStatus',
    'Name',
    'QualificationTypeId'])

d = d.drop(labels = ['Name'], axis = 1)
stim = pd.read_csv("stimuli/OrderB.csv")
stim = stim.rename(columns={"LIST_ID": "ListId"})
d = d.merge(stim, how='left')
d = d.loc[:,[
    'WorkerId',
    'HITId',
    'AssignmentId',
    'AssignmentStatus',
    'QualificationTypeId',
    'ListId',
    'CUE_ID',
    'CUE',
    'R1',
    'R2',
    'R3'
]]


if not os.path.exists('new-responses-to-approve'):
    os.mkdir('new-responses-to-approve')
for aid in d['AssignmentId'].unique():
    z = d['AssignmentId'] == aid
    d[z].to_csv('new-responses-to-approve/{:s}.csv'.format(aid), index=False)

#m = d.loc[:,[
#    'WorkerId',
#    'HITId',
#    'AssignmentId',
#    'AssignmentStatus']].drop_duplicates()
#
#m.to_csv('Responses_EvaluationSheet.csv', index=False)

print("* ====")
print("* Submitted (not accepted or rejected) responses are written into:")
print("* ./new-responses_to_approve/")
print("*")
print("* Approve or reject each assignment by running:")
print("* python EvaluateResponses.py")
print("* ====")
print("")
