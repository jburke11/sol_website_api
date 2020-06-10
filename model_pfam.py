from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database_models import Model_pfam
from Bio import SeqIO
base = declarative_base()
engine = create_engine ( 'sqlite:////Users/burkej24/Desktop/potato_website/DM_6.1.db')
base.metadata.create_all ( engine )
Session = sessionmaker ( engine )
session = Session ( )

with open("DM_v6_1.working_models.pep.all.sort.pfam", "r") as in_pfam:
    for line in in_pfam:
        line = line.rstrip().split()
        print(line)
        model = Model_pfam(transcript_id=line[0], protein_match_start=line[1], protein_match_end=line[2],hmm_acc=line[5],
                           hmm_match_start=line[8], hmm_name=line[6], hmm_match_end=line[9], hmm_type=line[7],
                           bit_score=line[11], evalue=line[12])
        session.add(model)
    session.commit()
