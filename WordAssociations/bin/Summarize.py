#!/usr/bin/env python

import pandas as pd
import os
import sys

def Summarize(QDATA):
    if not os.path.exists("summary"):
        os.mkdir("summary")

    d = pd.read_csv(QDATA,header=[0,1,2],low_memory=False)
    d.columns = d.columns.droplevel(level=-1).droplevel(level=-1)
    z = pd.isnull(d['HIT_ID']).values

    d = d.loc[~z,('HIT_ID','ASSIGNMENT_ID','MTURK_ID','LIST_ID')]
    d.loc[:,'LIST_ID'] = d['LIST_ID'].astype(int)
    d.to_csv(os.path.join('summary','assignments.csv'),index=False)

    workers = d.groupby(['MTURK_ID']).size().reset_index(name='count')
    workers.to_csv(os.path.join('summary','workers.csv'),index=False)

    hits = d.groupby(['LIST_ID','HIT_ID']).size().reset_index(name='count')
    hits.to_csv(os.path.join('summary','hits.csv'),index=False)

    lists = d.groupby(['LIST_ID']).size().reset_index(name='count')
    lists.to_csv(os.path.join('summary','lists.csv'),index=False)

if __name__== "__main__":
    try:
        QDATA = sys.argv[1]
    except:
        print("Usage: Summarize.py <qualtrics-csv>")
        sys.exit(1)

    Summarize(QDATA)
