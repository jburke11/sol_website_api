from database_models import  Model_anno, Model_anno_seq, Model_iprscan,  Model_go_slim, Model_pfam, Putative_ssr
from sqlalchemy import and_, asc

def fetch_models(locus, session):
    query = session.query ( Model_anno.transcript_id ).filter ( Model_anno.gene_id == locus )
    models = [ ]
    for item in query :
        temp_dict = {}
        temp_dict [ "id" ] = item.transcript_id
        models.append ( temp_dict )
    return models

def fetch_putative_function(rep_model, session):
    query = session.query ( Model_anno.func_anno ).filter ( Model_anno.transcript_id == rep_model)
    query = query.first()
    return query.func_anno
'''
def fetch_blastp_hits(rep_model, session):
    query = session.query ( Model_uniref ).filter ( Model_uniref.transcript_id == rep_model ).order_by(asc ( Model_uniref.pvalue ) )
    models = [ ]
    for item in query :
        temp_dict = { }
        temp_dict [ "accession" ] = item.accession
        temp_dict [ "per_sim" ] = item.per_sim
        temp_dict [ "per_cov" ] = item.per_cov
        temp_dict [ "p_val" ] = item.pvalue
        temp_dict [ "description" ] = item.description [ 0 :60 ]
        models.append ( temp_dict )
    return models
    '''
def fetch_interpro(rep_model, session):
    query = session.query(Model_iprscan).filter(Model_iprscan.transcript_id == rep_model).order_by(asc(Model_iprscan.match_start))
    models = []
    for item in query:
        temp_dict = {}
        temp_dict["accession"] = item.interpro_accession
        temp_dict["method"] = item.method
        temp_dict["description"] = item.method_description
        temp_dict["match_start"] = item.match_start
        temp_dict["match_end"] = item.match_end
        models.append(temp_dict)
    return models
def fetch_go_annotation(rep_model, session):
    query = session.query(Model_go_slim).filter(Model_go_slim.transcript_id == rep_model)
    models = []
    for item in query:
        temp_dict = {}
        if item.go_type == "C":
            temp_dict [ "go_type" ] = "cellular component"
        elif item.go_type == "F":
            temp_dict [ "go_type" ] = "molecular function"
        elif item.go_type == "P":
            temp_dict [ "go_type" ] = "biological process"
        else:
            temp_dict [ "go_type" ] = "N/A"
        temp_dict["accession"] = item.go_accession
        temp_dict["go_name"] = item.go_name
        temp_dict["go_ev_code"] = item.go_ev_code
        temp_dict["go_dbxref"] = item.go_dbxref
        models.append(temp_dict)
    return models

def fetch_pfam(rep_model, session):
    query = session.query(Model_pfam).filter(Model_pfam.transcript_id == rep_model)
    models = []
    for item in query:
        temp_dict = {}
        temp_dict["hmm_acc"] = item.hmm_acc
        temp_dict["hmm_name"] = item.hmm_name
        temp_dict["protein_match_start"] = item.protein_match_start
        temp_dict["protein_match_end"] = item.protein_match_end
        temp_dict["evalue"] = item.evalue
        models.append(temp_dict)
    return models
def fetch_model_attrs(rep_model, session):
    query = session.query(Model_anno, Model_anno_seq).filter(Model_anno.transcript_id == Model_anno_seq.transcript_id).filter(Model_anno.transcript_id == rep_model)
    for anno, seq in query:
        if anno.origin == "+":
            end5 = anno.start
            end3 = anno.stop
        elif anno.origin == "-":
            end5 = anno.stop
            end3 = anno.start
        else:
            raise KeyError
        temp_dict = {}
        temp_dict["jbrowse_end5"] = anno.start - 500
        temp_dict["jbrowse_end3"] = anno.stop + 500
        temp_dict["end5"] = end5
        temp_dict["end3"] = end3
        temp_dict["nuc_length"] = len(seq.cds)
        temp_dict["prot_length"] = len(seq.protein.rstrip())
        temp_dict["scaffold"] = anno.scaffold
        return temp_dict
'''
def fetch_fpkm(rep_model, session):
    query = session.query(Model_FPKM).filter(Model_FPKM.transcript_id == rep_model)
    models = []
    for item in query:
        temp_dict = {}
        temp_dict["library"] = item.lib
        temp_dict["fpkm"] = item.fpkm
        models.append(temp_dict)
    return models
'''
def fetch_putataive_ssr(rep_model, end5, end3, session):
    query = session.query(Putative_ssr).filter(Putative_ssr.ssr_id == rep_model)
    models = []
    for item in query:
        res_dict = {}
        res_dict["end5"] = item.end5 + end5
        res_dict["scaffold"] = item.ref_seq
        res_dict["end3"] = item.end3 + end3
        res_dict["motif"] = item.motif.upper()
        res_dict["ssr_length"] = item.ssr_length
        models.append(res_dict)
    print(models)
    return models
def fetch_gene_model_sequences(rep_model, locus, session):
    query = session.query(Model_anno_seq).filter(Model_anno_seq.transcript_id == rep_model)
    res_dict = {}
    query = query.first()
    res_dict [ "cdna_seq" ] = ">" + rep_model + "|cDNA\n" + clean_sequence(query.cdna)
    res_dict["cds_seq"] = ">" + rep_model + "|cDNA\n" + clean_sequence(query.cds)
    res_dict["prot_seq"] = ">" + rep_model + "|cDNA\n" + clean_sequence(query.protein)
    #query = session.query ( Locus_anno_seq ).filter ( Locus_anno_seq.locus_id == locus )
    #query = query.first()
    #res_dict [ "locus_seq" ] = ">" + locus + "|genomic\n" + clean_sequence(query.locus)
    return res_dict

def fetch_gene_model_sequences_api(rep_model, locus, session):
    query = session.query(Model_anno_seq).filter(Model_anno_seq.transcript_id == rep_model)
    res_dict = {}
    query = query.first()
    res_dict [ "cdna_seq" ] = ">" + rep_model + "|cDNA\n" + query.cdna
    res_dict["cds_seq"] = ">" + rep_model + "|cDNA\n" + query.cds
    res_dict["prot_seq"] = ">" + rep_model + "|cDNA\n" + query.protein
    #query = session.query ( Locus_anno_seq ).filter ( Locus_anno_seq.locus_id == locus )
    #query = query.first()
    #res_dict [ "locus_seq" ] = ">" + locus + "|genomic\n" + clean_sequence(query.locus)
    return res_dict


def clean_sequence(sequence):
    result = ""
    x = 0
    y = 60
    while (x < len(sequence)):
        result += sequence[x:y] + '\n'
        x += 60
        y += 60
    return result

def reverse_complement(ch):
    if ch == "A" :
        return "T"
    elif ch == "T" :
        return "A"
    elif ch == "G" :
        return "C"
    else:
        return "G"