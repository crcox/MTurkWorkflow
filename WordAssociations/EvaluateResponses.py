#!/usr/bin/env python

import pandas as pd
import json
import glob
import os
import sys

edir = 'new-responses-to-approve'
flist = glob.glob(os.path.join(edir, '*.csv'))
#oldlist = glob.glob(os.path.join(edir,'approve', '*.json')) + glob.glob(os.path.join(edir,'reject', '*.json'))
#print(oldlist)
#if oldlist:
#    print("It looks like you've already evaluated some or all of these data.")
#    startover = input("Do you want to delete these decisions and start over?")
#    while not startover[0].lower() in ['y','n']:
#        print('Sorry, I did not understand that response. Please respond with [y]es or [n]o.')
#        startover = input("Do you want to delete these decisions and start over?")
#
#    if startover:
#        for f in oldlist:
#            os.remove(f)
#            print("Removed {:s}".format(f))
#
#    else:
#        print("Since you have chosen not to start fresh, let's not proceed.")
#        print("Exiting ...")
#        sys.exit(0)
#

to_approve = []
to_reject = []
if not os.path.exists(os.path.join(edir,'approve')):
    os.mkdir(os.path.join(edir,'approve'))

if not os.path.exists(os.path.join(edir,'reject')):
    os.mkdir(os.path.join(edir,'reject'))

for infile in flist:
    d = pd.read_csv(infile)
    a = d.loc[0,'AssignmentId']
    w = d.loc[0,'WorkerId']
    h = d.loc[0,'HITId']
    x = {'AssignmentId'      : a,
         'RequesterFeedback' : '',
         'OverrideRejection' : True}
    print("{key:12s}: {value:s}".format(key="AssignmentId", value=a))
    print("{key:12s}: {value:s}".format(key="WorkerId", value=w))
    print("{key:12s}: {value:s}".format(key="HITId", value=h))
    print("----")
    z = d['AssignmentId'] == a
    print(d.loc[z,('CUE','R1','R2','R3')])
    print("")
    approve = input("Do you approve this work? (y/n):")
    while not approve[0].lower() in ['y','n']:
        print('Sorry, I did not understand that response. Please respond with [y]es or [n]o.')
        approve = input("Do you approve this work? (y/n):")

    if approve[0] == 'y':
        with open(os.path.join(edir,'approve',a+'.json'),'w') as f:
            json.dump(x, f, indent=4, ensure_ascii=True)
            to_approve.append(a)

    else:
        print("Please briefly (one sentence) explain why you are rejecting this work.")
        x['RequesterFeedback'] = input("feedback: ")
        with open(os.path.join(edir,'reject',a+'.json'),'w') as f:
            json.dump(x, f, indent=4, ensure_ascii=True)
            to_reject.append(a)

    os.remove(infile)
    print('\n'*10)


print('* ====')
print("* You have accepted {:d} and rejected {:d} assignments.".format(len(to_approve),len(to_reject)))
print('* ')
print('* To submit your evaluations to MTurk, run ./SubmitEvaluations.sh.')
print('* ====')
