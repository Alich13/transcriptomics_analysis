#!/usr/bin/env python3le
import requests
import json
import pandas as pd
import subprocess

def get_control_accession(accession_sample):
    url='https://www.encodeproject.org/experiments/'+accession_sample+'/?format=json'
    r = requests.get(url, allow_redirects=True)
    x=json.loads(r.content)
    control_accession=x["possible_controls"][0]["accession"]
    return control_accession


df=pd.read_excel("/home/ali/PycharmProjects/transcriptomics_analysis/data/ENCODE_list.xlsx")

for index, row in (df.iloc[0:1].iterrows()):  #change range
        accession_sample = row['Accession']
        description=row["Description"]
        title=row["Assay title"]
        cell=row["Biosample term name"]
        target=row["Assay title"]
        dir_path = "/home/ali/PycharmProjects/transcriptomics_analysis/results/encode/" + description
        dir_path=dir_path.replace(" ", "_").replace("(","").replace(")","")
        dir_path_control = dir_path + "/control"
        accession_control= get_control_accession(accession_sample)
        print(dir_path_control)

        #download sample fastq and metadata.tsv

        url = 'https://www.encodeproject.org/batch_download/?type=Experiment&accession='+accession_sample+'&files.output_category=raw%20data&files.output_type=reads&files.status=released'
        r = requests.get(url, allow_redirects=True)
        subprocess.call('mkdir '+dir_path, shell=True)
        p = subprocess.Popen('cd '+dir_path +' && xargs -L 1 curl -O -J -L', shell=True, stdout = subprocess.PIPE, stdin = subprocess.PIPE)
        p.stdin.write(r.content)

        #download controls

        url = 'https://www.encodeproject.org/batch_download/?type=Experiment&accession='+accession_control+'&files.output_category=raw%20data&files.output_type=reads&files.status=released'
        r = requests.get(url, allow_redirects=True)
        subprocess.call('mkdir '+dir_path_control, shell=True)
        p = subprocess.Popen('cd ' + dir_path_control + ' && xargs -L 1 curl -O -J -L', shell=True, stdout=subprocess.PIPE,stdin=subprocess.PIPE)
        p.stdin.write(r.content)









