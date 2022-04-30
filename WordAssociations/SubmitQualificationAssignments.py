#!/usr/bin/env python

import glob
import os.path
import subprocess

def SubmitQualificationAssignments():
    to_qualify = glob.glob(os.path.join('new-qualification-assignments',"????_??.json"))
    print("Submitting {n:d} qualifications (two per assignment):".format(n=len(to_qualify)))
    for f in to_qualify:
        fstring = "file://{f:s}".format(f=f)
        result = subprocess.run([
            'aws','mturk','associate-qualification-with-worker',
            '--cli-input-json', fstring])

        if result.returncode == 0:
            os.remove(f)
            print("removed '{f:s}'".format(f=f))

    print("")
    print("* ===")
    print("* Qualifications successfully submitted. Participants will be barred from")
    print("* responding to the same list of cue words.")
    print("* ===")
    print("")

if __name__== "__main__":
    SubmitQualificationAssignments()
