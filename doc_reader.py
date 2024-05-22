# from unstructured.partition.pdf import partition_pdf
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def chunks_to_df(chunks):
    import pandas as pd
    df = pd.DataFrame(data=chunks, columns=['chunks'])
    return df

def clean_text(s_list):
    import re
    
    clean_list = []
    
    for s in s_list:
        s = re.sub(r"\.{4,}", "", s)
        s = re.sub(r"\d\.\d\w(\.\d|)", "", s)
        if len(s.strip()) > 1:
            clean_list.append(s)
        
    return clean_list

def read_document(filepath, chunk_size=100):
    from text_extract import create_store
    from langchain_text_splitters import SpacyTextSplitter
    
    store = create_store(filepath)
    text_splitter = SpacyTextSplitter(chunk_size = chunk_size, chunk_overlap=0)
    chunks = []
    for s in store:
        chunks += text_splitter.split_text(s)
    chunks = clean_text(chunks)
    chunk_df = chunks_to_df(chunks)
    os.remove(filepath)
    return chunk_df