#!/usr/bin/env python

import argparse
import pandas as pd
import sys
from lib.utils import read_qualtrics

parser = argparse.ArgumentParser(description='Return data by key.')
parser.add_argument('--key', type=str, help='an integer for the accumulator')
parser.add_argument('--value', type=str, help='sum the integers (default: find the max)')
args = parser.parse_args()

d = read_qualtrics('data/Word-Associations_MTurk.csv', melt = False)
if args.value == 'NA':
    z = d[args.key].isnull()
else:
    z = d[args.key] == args.value

print(d.loc[z,('WorkerId','HITId','AssignmentId','ListId','AssignmentStatus')])

