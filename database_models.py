from sqlalchemy import String, Integer, Column, create_engine, and_, ForeignKey, ForeignKeyConstraint, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
base = declarative_base()
engine = create_engine ( 'sqlite:////Users/burkej24/Desktop/trifida_anno_v3.db', echo=True)
class Model_anno(base):
    __tablename__ = 'model_anno'

    transcript_id = Column('transcript_id', String)
    gene_id = Column('gene_id', String, primary_key=True)
    scaffold = Column('scaffold', String)
    origin = Column('ori', String)
    start = Column('start',Integer,primary_key= True)
    stop = Column ('stop', Integer )
    is_repr = Column('is_repr', String)
    func_anno = Column('func_anno', String)
class Model_anno_seq(base):
    __tablename__ = 'model_anno_seq'
    transcript_id = Column("transcript_id", String, primary_key=True)
    cdna = Column('cdna', String)
    cds = Column('cds', String)
    protein = Column('protein', String)

class Locus_anno_seq(base):
    __tablename__ = "locus_anno_seq"
    locus_id = Column ( 'locus_id' , String, primary_key=True )
    locus = Column ( 'locus' , String )

class Model_go_slim(base):
    __tablename__ = 'model_go_slim'
    transcript_id = Column("transcript_id", String)
    go_accession = Column("go_accession", String)
    go_type = Column("go_type", String)
    go_name = Column("go_name", String, primary_key=True)
    go_ev_code = Column("go_ev_code", String)
    go_dbxref = Column("go_dbxref", String)

class Putative_ssr(base):
    __tablename__ = "putative_ssr"
    ssr_id = Column("ssr_id", String)
    ref_seq = Column("ref_seq", String)
    end5 = Column("end5", Integer, primary_key=True)
    end3 = Column("end3", Integer)
    unit_size = Column("unit_size", Integer)
    motif = Column("motif", String)
    length = Column("ssr_length", Integer)

class Model_uniref(base):
    __tablename__ = 'model_uniref'
    transcript_id = Column("transcript_id", String)
    accession = Column("accession", String, primary_key=True)
    per_sim = Column("per_sim", Float)
    per_cov = Column("per_cov", Float)
    pvalue = Column("pvalue", Float)
    description = Column("description", String)

class Model_iprscan(base):
    __tablename__= "model_iprscan"
    transcript_id = Column("transcript_id", String)
    method = Column("method", String)
    method_accession = Column("method_accession", String)
    method_description = Column("method_description", String)
    match_start = Column("match_start", Integer, primary_key=True)
    match_end = Column("match_end", Integer)
    evalue = Column("evalue", Float)
    interpro_accession = Column("interpro_accession", String)
    interpro_description = Column("interpro_description", String)
    interpro_go = Column("interpro_go", String)

class Model_pfam(base):
    __tablename__ = "model_pfam"
    transcript_id = Column("transcript_id", String, primary_key=True)
    protein_match_start = Column("protein_match_start", Integer)
    protein_match_end = Column("protein_match_end", Integer)
    hmm_acc = Column("hmm_acc", String)
    hmm_match_start = Column("hmm_match_start", Integer)
    hmm_match_end = Column("hmm_match_end", Integer)
    hmm_type = Column("hmm_type", String)
    bit_score = Column("bit_score", Float)
    evalue = Column("evalue", Float)
    hmm_name = Column("hmm_name", String)

class Model_FPKM(base):
    __tablename__ = "model_fpkm"
    transcript_id = Column("transcript_id", String)
    lib = Column("library", String)
    fpkm = Column("fpkm", Float, primary_key=True)
