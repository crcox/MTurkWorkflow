#!/usr/bin/env python

import os
import glob
import sys
import subprocess

if len(sys.argv) < 2:
    exp_dir = '.'
elif len(sys.argv) < 3:
    exp_dir = sys.argv[1]

to_approve = glob.glob(os.path.join(
    exp_dir,
    "new-responses-to-approve",
    "approve",
    "*.json"))
to_reject = glob.glob(os.path.join(
    exp_dir,
    "new-responses-to-approve",
    "reject",
    "*.json"))
print("Approving the following {n:d} assignments:".format(n=len(to_approve)))
for f in to_approve:
    fstring = "file://{f:s}".format(f=f)
    result = subprocess.run([
        'aws','mturk','approve-assignment',
        '--cli-input-json',fstring])

    if result.returncode == 0:
        os.remove(f)
        print("removed '{f:s}'".format(f=f))

print("")
print("Rejecting the following {n:d} assignments:".format(n=len(to_reject)))
for f in to_reject:
    fstring = "file://{f:s}".format(f=f)
    result = subprocess.run([
        'aws','mturk','reject-assignment',
        '--cli-input-json',fstring])

    if result.returncode == 0:
        os.remove(f)
        print("removed '{f:s}'".format(f=f))

print("")
print("* ===")
print("* Your evaluations have been submitted to MTurk. You may want to run:")
print("* python UpdateData.sh")
print("* so the status changes are reflected in")
print("* ./WordAssociations_MTurk.csv.")
print("* ===")
print("")
