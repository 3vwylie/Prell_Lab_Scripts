'''Input pisa-analysis' interface json file for extraction'''
import json
import argparse
import pandas as pd
import time
import glob

parser = argparse.ArgumentParser(
    prog='python check_checksum_sums.py',
    description='''TBD''')
parser.add_argument('--pretransfer')
parser.add_argument('--posttransfer')
args=parser.parse_args()

with open (args.pretransfer, "r", encoding='utf-8-sig') as file_:
    pre_lines = file_.readlines()
    dict_pre = {}
    for line in pre_lines:
        line = line.split("  ")
        dict_pre[line[1].strip()] = line[0]
        
with open (args.posttransfer, "r", encoding='utf-8-sig') as file_:
    post_lines = file_.readlines()
    dict_post = {}
    for line in post_lines:
        line = line.split("  ")
        dict_post[line[1].strip()] = line[0]
        
    #print(sorted(list_lines, key=lambda line_: line_[1]))
    
discrepancies = []
for key in list(dict_pre.keys()):
    if dict_pre[key] == dict_post[key]:
        del dict_pre[key]
        del dict_post[key]
    else:
        discrepancies.append([dict_pre[key], dict_post[key], key])
        del dict_pre[key]
        del dict_post[key]
        

if len(discrepancies) >= 1:
    for discrepancy in discrepancies:
        print(discrepancy)
else:
    print("Looks good!")