from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database_models import Putative_ssr, Model_anno
from Bio import SeqIO
base = declarative_base()
engine = create_engine ( 'sqlite:////Users/burkej24/Desktop/potato_website/DM_6.1.db')
base.metadata.create_all ( engine )
Session = sessionmaker ( engine )
session = Session ( )

with open("ssr.txt", "r") as in_ssr:
    for line in in_ssr:
        line = line.rstrip().split()
        query = session.query(Model_anno).filter(Model_anno.transcript_id == line[0])
        query = query.first()
        chr = query.scaffold
        print(chr)
        model = Putative_ssr(ssr_id=line[0], ref_seq=chr, end5=line[6], end3=line[5], unit_size=line[-1],
                             motif=line[3], ssr_length=line[3])
        session.add(model)
    session.commit()
