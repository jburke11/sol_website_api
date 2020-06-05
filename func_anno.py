# load Genome assembly for the doubled monoploid potato DM 1-3 516 R44 - v6.1 into table model_anno, is_repr and func_anno are set to null
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

with open("/Users/burkej24/Downloads/DM_1-3_516_R44_potato.v6.1.working_models.func_anno.txt") as func_anno_in:
    for line in func_anno_in:
        line = line.rstrip().split("\t")
        query = session.query(Model_anno).filter(Model_anno.transcript_id == line[0])
        query = query.first()
        try:
            query.func_anno = line[1]
            print(line[1])
        except:
            print(" not found")
            pass
session.commit()