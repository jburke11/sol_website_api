from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database_models import Model_go_slim, Model_anno, Model_iprscan
base = declarative_base()
engine = create_engine ( 'sqlite:////Users/burkej24/Desktop/potato_website/DM_6.1.db')
base.metadata.create_all ( engine )
Session = sessionmaker ( engine )
session = Session ( )

go_dict = {}
with open("go_slim.txt", "r") as go_in:
    go_in.readline()
    go_in.readline ( )
    go_in.readline ( )
    go_in.readline ( )
    for line in go_in:
        temp_dict = {}
        line = line.rstrip().split("\t")
        temp_dict["go_accession"] = line[5]
        temp_dict["go_type"] = line[7]
        temp_dict["go_name"] = line[8]
        temp_dict["go_ev_code"] = line[9]
        temp_dict["go_dbxref"] = "TAIR:" + line[0]
        go_dict[line[5]] = temp_dict
print("dictionary created")

query = session.query(Model_iprscan).filter(Model_iprscan.interpro_go != "NA")
count = 0
for item in query:
    try:
        transcript_id = item.transcript_id
        go_list = item.interpro_go.split("|")
        for go in go_list:
            temp = go_dict[go]
            model = Model_go_slim(transcript_id=transcript_id, go_accession=temp["go_accession"], go_type=temp["go_type"],
                                  go_name=temp["go_name"], go_ev_code=temp["go_ev_code"], go_dbxref=temp["go_dbxref"], count = count)
            count = count + 1
    except:
        print("error")
        count = count + 1
print(count)
