#populates empty table with transcript ids from model_anno
#parses cds,cdna,amino acid sequences and inserts them into the database based on transcript id
#
#
from sqlalchemy import String,Integer,Column, create_engine, and_, ForeignKey, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from database_models import Model_anno_seq, Model_anno
from Bio import SeqIO, SeqRecord, Seq
base = declarative_base()
engine = create_engine ( 'sqlite:////Users/burkej24/Desktop/potato_website/DM_6.1.db')
base.metadata.create_all ( engine )
Session = sessionmaker ( engine )
session = Session ( )

query = session.query(Model_anno.transcript_id)
for item in query:
    new_col = Model_anno_seq(transcript_id=item.transcript_id)
    session.add(new_col)
session.commit()
print("ids in")
for record in SeqIO.parse("/Users/burkej24/Downloads/DM_1-3_516_R44_potato.v6.1.hc_gene_models.cds.fa", "fasta"):
    query = session.query(Model_anno_seq).filter(Model_anno_seq.transcript_id == record.id)
    query = query.first()
    try:
        query.cds = str(record.seq)
    except:
        print("id not found")
print("cds done")
for record in SeqIO.parse("/Users/burkej24/Downloads/DM_1-3_516_R44_potato.v6.1.hc_gene_models.cdna.fa", "fasta"):
    query = session.query(Model_anno_seq).filter(Model_anno_seq.transcript_id == record.id)
    query = query.first()
    try:
        query.cdna = str(record.seq)
    except:
        print("id not found")
print("cdna done")
for record in SeqIO.parse("/Users/burkej24/Downloads/DM_1-3_516_R44_potato.v6.1.hc_gene_models.pep.fa", "fasta"):
    query = session.query(Model_anno_seq).filter(Model_anno_seq.transcript_id == record.id)
    query = query.first()
    try:
        query.protein = str(record.seq)
    except:
        print("id not found")
session.commit()
