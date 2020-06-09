# parse through iprscan tsv results and populate table model_iprscan
from sqlalchemy import String,Integer,Column, create_engine, and_, ForeignKey, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from database_models import Model_iprscan
base = declarative_base()
engine = create_engine ( 'sqlite:////Users/burkej24/Desktop/potato_website/DM_6.1.db')
base.metadata.create_all ( engine )
Session = sessionmaker ( engine )
session = Session ( )

with open("DM.pep.fa.tsv", "r") as in_tsv:
    for line in in_tsv:
        try:
            print("line")
            line = line.rstrip().split("\t")
            if line[8] == "-" or line[8] == "T":
                line[8] = None
            model = Model_iprscan(transcript_id=line[0], method=line[3], method_accession=line[4], method_description=line[5],\
                                  match_start=line[6], match_end=line[7], evalue=line[8], interpro_accession=line[11],\
                                  interpro_description=line[12], interpro_go=line[13])
            session.add ( model )
        except IndexError:
            if line[8] == "-" or line[8] == "T":
                line[8] = None
            length = len(line)
            if "2020" in line[-1]:
                model = Model_iprscan(transcript_id=line[0], method=line[3], method_accession=line[4], method_description=line[5],\
                                  match_start=line[6], match_end=line[7], evalue=line[8], interpro_accession="NA",\
                                  interpro_description="NA", interpro_go="NA")
            elif "IPR" in line[-1]:
                model = Model_iprscan ( transcript_id=line [ 0 ] , method=line [ 3 ] , method_accession=line [ 4 ] ,
                                        method_description=line [ 5 ] , \
                                        match_start=line [ 6 ] , match_end=line [ 7 ] , evalue=line [ 8 ] ,
                                        interpro_accession=line[11] , \
                                        interpro_description="NA" , interpro_go="NA" )
            else:
                model = Model_iprscan ( transcript_id=line [ 0 ] , method=line [ 3 ] , method_accession=line [ 4 ] ,
                                        method_description=line [ 5 ] , \
                                        match_start=line [ 6 ] , match_end=line [ 7 ] , evalue=line [ 8 ] ,
                                        interpro_accession=line[11] , \
                                        interpro_description=line[12] , interpro_go="NA" )
            session.add ( model )
    session.commit()
