#!/usr/bin/env python

import os
from bin.PullQualtrics import PullQualtrics
from bin.PullHITs import PullHITs
from bin.PullQualificationsKey import PullQualificationsKey
from bin.Summarize import Summarize

surveyID='SV_8cckNoJtSmQ0AUR'
fileFormat='csv'

PullQualtrics(surveyID,fileFormat)

if not os.path.exists("data"):
    os.mkdir("data")

if os.path.exists(os.path.join("data","Word-Associations_MTurk.csv" )):
    os.rename(
        os.path.join("data","Word-Associations_MTurk.csv"),
        os.path.join("data","Word-Associations_MTurk_Previous.csv"))

os.rename(
    os.path.join("MyQualtricsDownload","Word Associations: MTurk.csv"),
    os.path.join("data","Word-Associations_MTurk.csv"))

os.rmdir("MyQualtricsDownload")

Summarize("data/Word-Associations_MTurk.csv")
PullHITs()
PullQualificationsKey()

