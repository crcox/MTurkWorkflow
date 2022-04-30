#!/usr/bin/env python

import os
import subprocess

def PullHITs():
    hit_dir = os.path.join('data','HITS')
    if not os.path.exists(hit_dir):
        os.mkdir(hit_dir)

    with open(os.path.join('summary','hits.csv'), 'r') as f:
        header = f.readline()
        for line in f:
            hit = line.strip().split(',')[1]
            hit_json = os.path.join("data","HITS","{hit:s}.json".format(hit=hit))
            print("Retrieving assignments for HIT {hit:s} ...".format(hit=hit))
            with open(hit_json,'wb') as j:
                result = subprocess.run(["aws","mturk","list-assignments-for-hit","--hit-id",hit],stdout=j)
                #if result.returncode == 0:
                #    j.write(result.stdout)

            hit_definition_json = os.path.join("data","HITS","definition","{hit:s}.json".format(hit=hit))
            with open(hit_definition_json,'wb') as j:
                result = subprocess.run(["aws","mturk","get-hit","--hit-id",hit],stdout=j)


    print("* ===")
    print("* All assignments retrieved and written to 'data/HITS'.")
    print("* ===")

if __name__== "__main__":
    PullHITs()
