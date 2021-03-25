#!/usr/bin/env python3le
import requests
import json
import subprocess



def get_control_accession(accession_sample):
    url='https://www.encodeproject.org/experiments/'+accession_sample+'/?format=json'
    r = requests.get(url, allow_redirects=True)
    x=json.loads(r.content)
    control_accession=x["possible_controls"][0]["accession"]
    return control_accession


accession_sample ="ENCSR231PWH"
description="first_discription "
accession_control= get_control_accession(accession_sample)

url = 'https://www.encodeproject.org/batch_download/?type=Experiment&accession='+accession_sample+'&files.output_category=raw%20data&files.output_type=reads&files.status=released'
r = requests.get(url, allow_redirects=True)
dir_path="/home/ali/PycharmProjects/transcriptomics_analysis/results/encode/"+description
subprocess.call('mkdir '+dir_path, shell=True)
p = subprocess.Popen('cd '+dir_path +' && xargs -L 1 curl -O -J -L', shell=True, stdout = subprocess.PIPE, stdin = subprocess.PIPE)
p.stdin.write(r.content)



#subprocess.run(["cd /home/ali/PycharmProjects/transcriptomics_analysis/results/encode && xargs -L 1 curl -O -J -L < "
#                "/home/ali/PycharmProjects/transcriptomics_analysis/data/files_test.txt  "], shell=True)





