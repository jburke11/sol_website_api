from database_models import Model_anno,  engine, base, chr_seq, Model_anno_seq, Model_iprscan, Model_go_slim
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import re
from utility import fetch_models, fetch_putative_function, fetch_interpro, fetch_go_annotation, fetch_pfam,\
    fetch_model_attrs, fetch_putataive_ssr, fetch_gene_model_sequences, clean_sequence, reverse_complement, \
    fetch_gene_model_sequences_api
def start_connection():
    Session = sessionmaker(engine)
    session = Session()
    return session
def stop_session(session):
    session.close()
    return 1

base.metadata.create_all( engine )
app = FastAPI(debug = True , title="Potato Genome API Documentation") # debug will need to be changed to false

app.add_middleware(
    CORSMiddleware,
    allow_origins =  ['*'], # this needs to be changed when moving to prod. it will need to be the ip address of the website
    allow_methods = ['*'],
    allow_headers = ['*'], # probably needs to be changed also
    max_age = 1
)

@app.get("/")
def root():
    return {"Status" : "Operational"}


@app.get("/id/{transcript_id}")
def get_id(transcript_id: str):
    try:
        item_id = transcript_id.rstrip()
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


@app.get("/api/id/{transcript_id}")
def get_id(transcript_id: str):
    try:
        item_id = transcript_id.rstrip()
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
        data["sequences"] = fetch_gene_model_sequences_api(rep_model, data["locus"], session)
        if len(data) == 0:
            raise KeyError
        return data
    except KeyError:
        print("error")
        raise HTTPException(status_code=404, detail="id not found")
    finally:
        stop_session(session)

@app.get("/function/{function}")
def get_function(function: str):
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
            temp_dict["species"] = "S. tuberosum Group Phureja DM 1-3 516 R44"
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
                temp_dict["species"] = "S. tuberosum Group Phureja DM 1-3 516 R44"
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
                temp_dict [ "species" ] = "S. tuberosum Group Phureja DM 1-3 516 R44"
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



@app.get("/go/{keyword}-{type}")
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
                temp_dict["species"] = "S. tuberosum Group Phureja DM 1-3 516 R44"
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
                temp_dict [ "species" ] = "S. tuberosum Group Phureja DM 1-3 516 R44"
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

@app.get("/seq/{chr}-{start}-{stop}")
def get_from_length(chr:str, start: int, stop: int):
  session = start_connection()
  query = session.query(chr_seq).filter(chr_seq.chr == chr)
  seq = query.one()
  if seq.length < stop or start < 1:
      raise HTTPException( status_code=404 , detail="sequence not found")
  else:
      data = {}
      data ["chr"] = seq.chr
      data["seq"] = clean_sequence(seq.seq[start:stop])
      data["head"] = ">" + seq.chr + ":" + str(start) + "," + str(stop)
      stop_session(session)
      return data

@app.get ( "/api/seq/{chr}-{start}-{stop}" )
def get_from_length(chr: str , start: int , stop: int) :
    session = start_connection ( )
    query = session.query ( chr_seq ).filter ( chr_seq.chr == chr )
    seq = query.one ( )
    if seq.length < stop or start < 1 :
        raise HTTPException ( status_code=404 , detail="sequence not found" )
    else :
        data = { }
        data ["chr"] = seq.chr
        data ["seq"] = seq.seq [start :stop]
        data ["head"] = ">" + seq.chr + ":" + str ( start ) + "," + str ( stop )
        stop_session ( session )
        return data

@app.get("/seq/{id}-{type}")
def get_seq_from_id(id: str, type: str):
    session = start_connection()
    try:
        if type == "Transcript":
            query = session.query(Model_anno_seq).filter(Model_anno_seq.transcript_id == id)
            query = query.one()
            data = {}
            data["seq"] = clean_sequence(query.cdna)
            data["head"] = ">" + query.transcript_id
            return data
        elif type == "CDS":
            query = session.query ( Model_anno_seq ).filter ( Model_anno_seq.transcript_id == id )
            query = query.one ( )
            data = { }
            data ["seq"] = clean_sequence(query.cds)
            data ["head"] =">" + query.transcript_id
            return data
        else:
            query = session.query ( Model_anno_seq ).filter ( Model_anno_seq.transcript_id == id )
            query = query.one ()
            data = { }
            data ["seq"] = clean_sequence(query.protein)
            data ["head"] = ">" + query.transcript_id
            return data
    except:
        raise HTTPException(status_code=404 , detail="transcript id not found")
    finally:
        stop_session(session)

@app.get("/api/seq/{id}-{type}")
def get_seq_from_id(id: str, type: str):
    session = start_connection()
    try:
        if type == "Transcript":
            query = session.query(Model_anno_seq).filter(Model_anno_seq.transcript_id == id)
            query = query.one()
            data = {}
            data["seq"] = query.cdna
            data["head"] = ">" + query.transcript_id
            return data
        elif type == "CDS":
            query = session.query ( Model_anno_seq ).filter ( Model_anno_seq.transcript_id == id )
            query = query.one ( )
            data = { }
            data ["seq"] = query.cds
            data ["head"] =">" + query.transcript_id
            return data
        else:
            query = session.query ( Model_anno_seq ).filter ( Model_anno_seq.transcript_id == id )
            query = query.one ()
            data = { }
            data ["seq"] = query.protein
            data ["head"] = ">" + query.transcript_id
            return data
    except:
        raise HTTPException(status_code=404 , detail="transcript id not found")
    finally:
        stop_session(session)

@app.get("/seq_dir/{bp}-{direction}-{id}")
def get_seq_from_direction(bp: int, direction: str, id: str):
    session = start_connection()
    session_query = sqlite3.connect("/Users/burkej24/Desktop/potato_website/DM_6.1.db")
    try:
        query = session.query(Model_anno).filter(Model_anno.transcript_id == id)
        query = query.one()
        start = query.start
        stop = query.stop
        chr = query.scaffold
        query1 = session.query(chr_seq.length).filter(chr_seq.chr == chr)
        length = query1.one()[0]
        if length < 1:
            raise IndexError
        data = {}
        if direction == "upstream":
            if stop + bp > length:
                raise IndexError
            items = (str(stop), str(bp), str(chr))
            big_seq = session_query.execute (
                "select substr(chr_seq.seq, ?,?) from chr_seq where chr_seq.chr == ?", items)
            seq = str(big_seq.fetchone()[0])
            if query.origin == "-":
                seq = seq[::-1]
                seq = ("").join([reverse_complement(ch) for ch in seq])
            else:
                pass
            data["seq"] = clean_sequence(seq)
            data["caption"] = id + " was found on " + chr + " from " + str(start) + " to " + str(stop) + "\n" + "Displaying " + str(bp) + " bp " + direction \
            + " of " + id + " from position " + str(stop) + " to " + str(stop + bp)
            data["head"] = ">" + chr + ":" + str(stop) + "," + str(stop+bp)
        else:
            if start - bp < 1:
                raise IndexError
            items = (str ( start - bp ) ,str ( bp ), chr)
            big_seq = session_query.execute (
                "select substr(chr_seq.seq, ?,?) from chr_seq where chr_seq.chr == ?", items )
            seq = str(big_seq.fetchone()[0])
            if query.origin == "-":
                seq = seq[::-1]
                seq = ("").join([reverse_complement(ch) for ch in seq])
            else:
                pass
            data ["seq"] = clean_sequence(seq)
            data["caption"] = id + " was found on " + chr + " from " + str(start) + " to " + str(stop) + "\n" + "Displaying " + str(bp) + " bp " + direction \
            + " of " + id + " from position " + str(start - bp) + " to " + str(start)
            data["head"] = ">" + chr + ":" + str(start - bp) + "," + str(start)
        return data
    except IndexError:
        raise HTTPException ( status_code=404 , detail="transcript id not found" )
    finally:
        stop_session ( session )
        session_query.close()

@app.get("/api/seq_dir/{bp}-{direction}-{id}")
def get_seq_from_direction(bp: int, direction: str, id: str):
    session = start_connection()
    session_query = sqlite3.connect("/Users/burkej24/Desktop/potato_website/DM_6.1.db")
    try:
        query = session.query(Model_anno).filter(Model_anno.transcript_id == id)
        query = query.one()
        start = query.start
        stop = query.stop
        chr = query.scaffold
        query1 = session.query(chr_seq.length).filter(chr_seq.chr == chr)
        length = query1.one()[0]
        if length < 1:
            raise IndexError
        data = {}
        if direction == "upstream":
            if stop + bp > length:
                raise IndexError
            items = (str(stop), str(bp), str(chr))
            big_seq = session_query.execute (
                "select substr(chr_seq.seq, ?,?) from chr_seq where chr_seq.chr == ?", items)
            seq = str(big_seq.fetchone()[0])
            if query.origin == "-":
                seq = seq[::-1]
                seq = ("").join([reverse_complement(ch) for ch in seq])
            else:
                pass
            data["seq"] = seq
            data["caption"] = id + " was found on " + chr + " from " + str(start) + " to " + str(stop) + "\n" + "Displaying " + str(bp) + " bp " + direction \
            + " of " + id + " from position " + str(stop) + " to " + str(stop + bp)
            data["head"] = ">" + chr + ":" + str(stop) + "," + str(stop+bp)
        else:
            if start - bp < 1:
                raise IndexError
            items = (str ( start - bp ) ,str ( bp ), chr)
            big_seq = session_query.execute (
                "select substr(chr_seq.seq, ?,?) from chr_seq where chr_seq.chr == ?", items )
            seq = str(big_seq.fetchone()[0])
            if query.origin == "-":
                seq = seq[::-1]
                seq = ("").join([reverse_complement(ch) for ch in seq])
            else:
                pass
            data ["seq"] = seq
            data["caption"] = id + " was found on " + chr + " from " + str(start) + " to " + str(stop) + "\n" + "Displaying " + str(bp) + " bp " + direction \
            + " of " + id + " from position " + str(start - bp) + " to " + str(start)
            data["head"] = ">" + chr + ":" + str(start - bp) + "," + str(start)
        return data
    except IndexError:
        raise HTTPException ( status_code=404 , detail="transcript id not found" )
    finally:
        stop_session ( session )
        session_query.close()

@app.get("/find_transcripts/{locus}")
def gene_to_transcript(locus: str):
    try:
        session = start_connection()
        query = session.query(Model_anno.transcript_id).filter(Model_anno.gene_id == locus)
        data = {}
        data["transcripts"] = []
        for item in query:
            print("here")
            data["transcripts"].append(item[0])
        return data
    except:
        raise HTTPException ( status_code=404 , detail="transcript id not found" )
    finally:
        stop_session(session)
