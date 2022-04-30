#!/usr/bin/env python

import pandas as pd
import numpy as np
import sys
import tempfile
import os.path
from lib.utils import read_qualtrics

M = read_qualtrics(os.path.join('data','Word-Associations_MTurk.csv'), melt = False, meta = True)

exceptions = pd.read_csv('data/exceptions.csv')

z = exceptions['AssignmentStatus'] == 'Approved'
exceptions = exceptions.loc[z,:]
for i, row in exceptions.iterrows():
    z = M.loc[:,'WorkerId'] == row['WorkerId']
    z = z & M.loc[:,'HITId'] == row['HITId']
    z = z & M.loc[:,'AssignmentId'] == row['AssignmentId']
    M.loc[z,'AssignmentStatus'] = row['AssignmentStatus']

col_order = [
    "WorkerId","HITId","AssignmentId","ListId","AssignmentStatus","Duration (in seconds)","RecordedDate",
    "ResponseId","LocationLatitude","LocationLongitude","DistributionChannel","UserLanguage","DOB",
    "EduLevel","Gender","IncomeLevel","Race","Ethnicity","Parent","Interact","Interact_Freq","Feedback"]
M = M.reindex(col_order, axis=1)
z = M.loc[:,'AssignmentStatus'] == 'Approved'
M = M.loc[z,:]
M.to_csv(os.path.join("data", "approved_metadata.csv"), index=False)
