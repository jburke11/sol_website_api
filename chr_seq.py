from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database_models import chr_seq
from Bio import SeqIO
base = declarative_base()
engine = create_engine ( 'sqlite:////Users/burkej24/Desktop/potato_website/DM_6.1.db')
base.metadata.create_all ( engine )
Session = sessionmaker ( engine )
session = Session ( )
"""
for record in SeqIO.parse("/Users/burkej24/Downloads/DM_1-3_516_R44_potato_genome_assembly.v6.1.fa", "fasta"):
    seq = str(record.seq)
    length = len(seq)
    chr = record.id
    model = chr_seq(seq = seq, length = length, chr = chr)
    session.add(model)
session.commit()
"""
all_seq = ""
for record in SeqIO.parse("/Users/burkej24/Downloads/DM_1-3_516_R44_potato_genome_assembly.v6.1.fa", "fasta"):
    if "chr" in record.id:
        seq = str(record.seq)
        all_seq += seq
    else:
        pass
model = chr_seq(seq = all_seq, chr="all" , length=len(all_seq))
session.add(model)
session.commit()
session.close()