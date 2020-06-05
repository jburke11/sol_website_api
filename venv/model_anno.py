# load Genome assembly for the doubled monoploid potato DM 1-3 516 R44 - v6.1 into table model_anno, is_repr and func_anno are set to null
from sqlalchemy import String,Integer,Column, create_engine, and_, ForeignKey, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
base = declarative_base()
engine = create_engine ( 'sqlite:////Users/burkej24/Desktop/potato_website/DM_6.1.db', echo = True)
base.metadata.create_all ( engine )
Session = sessionmaker ( engine )
session = Session ( )
class Model_anno(base):
    __tablename__ = 'model_anno'

    transcript_id = Column('transcript_id', String, primary_key=True)
    gene_id = Column('gene_id', String)
    scaffold = Column('scaffold', String)
    origin = Column('ori', String)
    start = Column('start',Integer)
    stop = Column ('stop', Integer )
    is_repr = Column('is_repr', String)
    func_anno = Column('func_anno', String)

with open("/Users/burkej24/Downloads/DM_1-3_516_R44_potato.v6.1.hc_gene_models.gff3") as in_gff:
    for line in in_gff:
        lst = line.rstrip().split()
        if lst[2] == "mRNA":
            scaffold = lst[0]
            origin = lst[6]
            start = lst[3]
            stop = lst[4]
            description = lst[-1]
            desc_list = description.split(";")
            transcript_id = desc_list[0].split("=")[-1]
            gene_id = desc_list[2].split("=")[-1]
            new_column = Model_anno(transcript_id=transcript_id, gene_id=gene_id, scaffold=scaffold, origin=origin, start=start, stop=stop)
            session.add(new_column)
        else:
            pass
session.commit()
session.close()