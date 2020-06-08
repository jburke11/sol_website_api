# loads in representative transcripts
# parses those transcripts to find the match in the model_anno table and sets is_repr to Y
# parses the model_anno table again and sets all transcripts that are not representative to N
from sqlalchemy import String,Integer,Column, create_engine, and_, ForeignKey, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
base = declarative_base()
engine = create_engine ( 'sqlite:////Users/burkej24/Desktop/potato_website/DM_6.1.db')
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

with open("/Users/burkej24/Downloads/DM_1-3_516_R44_potato.v6.1.repr_hc_gene_models.gff3") as in_gff:
    for line in in_gff:
        line = line.rstrip().split()
        if line[2] == "mRNA":
            description = line[-1].split(";")
            transcript = description[0].split("=")[-1]
            query = session.query(Model_anno).filter(Model_anno.transcript_id == transcript)
            query = query.first()
            try:
                query.is_repr = "Y"
            except:
                print("not repr")
session.commit()

query = session.query(Model_anno)
for item in query:
    if item.is_repr != "Y":
        item.is_repr = "N"
    else:
        pass
session.commit()
