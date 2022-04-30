#!/usr/bin/env python

import argparse
import pandas as pd
import sys
from lib.utils import read_qualtrics

parser = argparse.ArgumentParser(description='Return data by key.')
parser.add_argument('--key', type=str, help='an integer for the accumulator')
parser.add_argument('--value', type=str, help='sum the integers (default: find the max)')
args = parser.parse_args()

d = read_qualtrics('data/Word-Associations_MTurk.csv', melt = True)
if args.value == 'NA':
    z = d[args.key].isnull()
else:
    z = d[args.key] == args.value

pd.set_option('display.max_rows', None)
for y,x in d.loc[z,:].groupby(by=['AssignmentId','WorkerId','HITId']):
    a = x.iloc[0]['AssignmentId']
    w = x.iloc[0]['WorkerId']
    h = x.iloc[0]['HITId']
    l = int(x.iloc[0]['ListId'])
    if pd.isnull(a):
        a = 'NA'
    if pd.isnull(w):
        w = 'NA'
    if pd.isnull(h):
        h = 'NA'
    if pd.isnull(l):
        l = 'NA'
    print("{key:12s}: {value:s}".format(key="AssignmentId", value=a))
    print("{key:12s}: {value:s}".format(key="WorkerId", value=w))
    print("{key:12s}: {value:s}".format(key="HITId", value=h))
    print("{key:12s}: {value:d}".format(key="ListId", value=l))
    print("----")
    z = d['AssignmentId'] == a
    print(x.loc[z,('CUE','R1','R2','R3')])
    print('')
    input('Press any key to continue.')

