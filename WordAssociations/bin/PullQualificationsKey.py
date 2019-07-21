#!/usr/bin/env python

import os
import subprocess

def PullQualificationsKey():
    print("Refreshing key to custom Qualification types ...")
    with open(os.path.join('data','MTurk-Qualification-Key.json'),'wb') as j:
        result = subprocess.run([
            'aws','mturk','list-qualification-types',
            '--no-must-be-requestable',
            '--must-be-owned-by-caller'],
            stdout=j)

    print("Updated key to custom Qualification types: 'data/MTurk-Qualification-Key.json'")

if __name__== "__main__":
    PullQualificationsKey()
