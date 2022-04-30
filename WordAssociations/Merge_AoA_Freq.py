#!/usr/bin/env python

import pandas as pd

d = pd.read_csv("./data/unique_responses.csv")
aoa = pd.read_excel("corpora/AoA_51715_words.xlsx")
aoa = aoa.rename({'Word':'RESPONSE'},axis='columns')
freq = pd.read_excel("corpora/SUBTLEXusfrequencyabove1.xls")
freq = freq.rename({'Word':'RESPONSE'},axis='columns')
# Merge in AOA and Frequency
d = d.merge(
    aoa.loc[:,['RESPONSE','AoA_Kup']],
    how='left',
    on='RESPONSE')
d = d.merge(
    freq.loc[:,['RESPONSE','SUBTLWF','Lg10WF','SUBTLCD','Lg10CD']],
    how='left',
    on='RESPONSE')

d.to_csv("./data/unique_responses_norms.csv", na_rep = '#N/A')
