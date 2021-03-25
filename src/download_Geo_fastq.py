import xml.etree.ElementTree as ET
from Bio import  Entrez
import pandas as pd
import subprocess
Entrez.email = "chemkhi.ali13@gmail.com"

def get_XML_summary (project_name) -> object:#PRJNA352669

    query = project_name+'[BioProject] AND "rna seq"[Strategy] AND "homo sapeins"[Organism]'
    search_handle = Entrez.esearch(db="sra", term=query, retmax=500, rettype="acclist")
    search_results = Entrez.read(search_handle)
    search_handle.close()
    IDs= search_results['IdList']
    fetch_handle = Entrez.efetch(
        db="sra",
        retstart=0,
        retmax=200,
        rettype="summary",
        id=IDs)
    record = fetch_handle.read()  # need to parse XML
    return record





if __name__ == '__main__' :
    df = pd.read_excel('/home/ali/PycharmProjects/transcriptomics_analysis/data/GEO -Filtred(AutoRecovered).xlsx')
    for index, row in (df.iloc[0:6].iterrows()):
        project=row['project']
        cell_type=row['CELL TYPE']
        txf=row['Target TXF']
        record=get_XML_summary(str(project))

        #parse Xml record

        root = ET.fromstring(record)
        for child in root:
            for experiment in child.findall('EXPERIMENT'):
                srx = experiment.get('accession')
                title = experiment.find('TITLE').text

                #run terminal commands here

                terminal_download="esearch -db sra -query "+srx+"[Accession]  | efetch --format runinfo | cut -d '," \
                                                                "' -f 1 | grep SRR |xargs fastq-dump -X 2 " \
                                                                "--split-files --outdir " \
                                                                "/home/ali/PycharmProjects/transcriptomics_analysis/results "

                subprocess.call(terminal_download, shell=True)

                terminal_change_name = 'cd /home/ali/PycharmProjects/transcriptomics_analysis/results ; for f in SRR* ; do ' \
                                       'mv -- "$f" '+'"'+title+'_${f%.fastq}_'+txf+'.fastq'+'"'+'; done '
                subprocess.call(terminal_change_name, shell=True)





                git_version ="addddd gggggggggggggggggggggg"
