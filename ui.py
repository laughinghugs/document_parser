import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from doc_reader import read_document
st.header("Document chunking")
with st.form("this_form"):
    uploaded_file = st.file_uploader("Choose a file")
    chunk_size = st.slider("Chunk size", min_value = 50, max_value = 1000, value = 350)
    submitted = st.form_submit_button("Submit")
    if submitted:
        bytes_data = uploaded_file.read()
        st.write("Uploaded filename:", uploaded_file.name)
        with open(f'data/tmp/{uploaded_file.name}', mode='wb') as w:
            w.write(bytes_data)
        df = read_document(f'data/tmp/{uploaded_file.name}', chunk_size)
        st.dataframe(df, use_container_width=True)
        