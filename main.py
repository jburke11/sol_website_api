from database_models import Model_anno,  engine, base
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import re
from utility import fetch_models, fetch_putative_function, fetch_interpro, fetch_go_annotation, fetch_pfam,\
    fetch_model_attrs, fetch_putataive_ssr, fetch_gene_model_sequences, Model_iprscan, Model_go_slim
def start_connection():
    Session = sessionmaker(engine)
    session = Session()
    return session
def stop_session(session):
    session.close()
    return 1

base.metadata.create_all( engine )
app = FastAPI(debug = True , title="Potato Genome API Documentation")

app.add_middleware(
    CORSMiddleware,
    allow_origins =  ['*'],
    allow_methods = ['*'],
    allow_headers = ['*'],
    max_age = 1
)

@app.get("/")
def root():
    return {"it" : "works"}


@app.get("/id/{item_id}")
def get_id(item_id: str):
    try:
        item_id = item_id.rstrip()
        session = start_connection()
        data = {}
        if re.match(r"^Soltu[.]DM[.]\d{2}G\d{6}[.]\d{1,2}$" , item_id):
            query = session.query(Model_anno.gene_id).filter(Model_anno.transcript_id == item_id)
            query = query.first()
            data["locus"] = query.gene_id
            data["rep_model"] = item_id
        elif re.match(r"^Soltu[.]DM[.]\d{2}G\d{6}$", item_id):
            data["locus"]= item_id
        else:
            raise KeyError
        if "rep_model" not in data:
            query = session.query(Model_anno.transcript_id).filter(and_(Model_anno.gene_id == data["locus"], Model_anno.is_repr == "Y"))
            query = query.first()
            data["rep_model"] = query.transcript_id
        else:
            pass
        rep_model = data["rep_model"]
        data["models"] = fetch_models(data["locus"], session)
        data["putative_function"] = fetch_putative_function(rep_model, session)
        #data["blastp"] = fetch_blastp_hits(rep_model, session)
        data["interpro"] = fetch_interpro(rep_model, session)
        data ["go"] = fetch_go_annotation(rep_model, session)
        data["pfam"] = fetch_pfam(rep_model, session)
        data["attrs"] = fetch_model_attrs(rep_model, session)
        #data["fpkm"] = fetch_fpkm(rep_model, session)
        data["putative_ssr"] = fetch_putataive_ssr(rep_model, data["attrs"]["end5"], data["attrs"]["end3"], session)
        data["sequences"] = fetch_gene_model_sequences(rep_model, data["locus"], session)
        if len(data) == 0:
            raise KeyError
        return data
    except KeyError:
        print("error")
        raise HTTPException(status_code=404, detail="id not found")
    finally:
        stop_session(session)

@app.get("/function/{function}-{species}")
def get_function(function: str, species:str):
    try:
        function = function.rstrip().split("_")
        function = " ".join(function)
        function = "%" + function + "%"
        session = start_connection()
        data = {}
        query = session.query(Model_anno).filter(Model_anno.func_anno.like(function))
        lst = []
        for item in query:
            temp_dict = {}
            temp_dict["species"] = species
            temp_dict["id"] = item.gene_id
            temp_dict["func"] = item.func_anno
            lst.append(temp_dict)
        data["func_search"] = lst
        data["length"] = len(data["func_search"])
        if len(data["func_search"]) == 0:
            raise KeyError
        return data
    except KeyError:
        raise HTTPException(status_code=404, detail="function not found")
    finally:
        stop_session(session)


@app.get("/interpro/{keyword}-{type}")
def get_interpro(keyword: str, type: str):
    try:
        session = start_connection()
        data = {}
        if type == "id":
            keyword = keyword.rstrip()
            query = session.query(Model_iprscan).filter(Model_iprscan.interpro_accession == keyword)
            lst = []
            for item in query:
                temp_dict = {}
                temp_dict["species"] = "all"
                temp_dict["sequence_id"] = item.transcript_id
                temp_dict["interpro_id"] = item.interpro_accession
                temp_dict["func_anno"] = item.method_description
                lst.append(temp_dict)
        else:
            keyword = keyword.rstrip ( ).split ( "_" )
            keyword = " ".join ( keyword )
            keyword = "%" + keyword + "%"
            query = session.query(Model_iprscan).filter(Model_iprscan.interpro_description.like(keyword))
            lst = []
            for item in query:
                temp_dict = { }
                temp_dict [ "species" ] = "all"
                temp_dict [ "sequence_id" ] = item.transcript_id
                temp_dict [ "interpro_id" ] = item.interpro_accession
                temp_dict [ "func_anno" ] = item.interpro_description
                lst.append ( temp_dict )
        data["interpro"] = lst
        if len(data["interpro"]) == 0:
            raise KeyError
        return data

    except KeyError:
        raise HTTPException ( status_code=404 , detail="function not found" )
    finally :
        stop_session ( session )



@app.get("/go/{keyword}-{type}") # function to get go results, still needs work
def get_go(keyword: str, type: str):
    try:
        session = start_connection()
        data = {}
        if type == "id":
            keyword = keyword.rstrip()
            query = session.query(Model_go_slim).filter(Model_go_slim.go_accession == keyword)
            lst = []
            for item in query:
                temp_dict = {}
                temp_dict["species"] = "all"
                temp_dict["sequence_id"] = item.transcript_id
                temp_dict["go_id"] = item.go_accession
                temp_dict["func_anno"] = item.go_name
                lst.append(temp_dict)
        else:
            keyword = keyword.rstrip ( ).split ( "_" )
            keyword = " ".join ( keyword )
            keyword = "%" + keyword + "%"
            query = session.query(Model_go_slim).filter(Model_go_slim.go_name.like(keyword))
            lst = []
            for item in query:
                temp_dict = { }
                temp_dict [ "species" ] = "all"
                temp_dict [ "sequence_id" ] = item.transcript_id
                temp_dict [ "go_id" ] = item.go_accession
                temp_dict [ "func_anno" ] = item.go_name
                lst.append ( temp_dict )
        data["go"] = lst
        if len(data["go"]) == 0:
            raise KeyError
        return data

    except KeyError:
        raise HTTPException ( status_code=404 , detail="function not found" )
    finally :
        stop_session ( session )
