
import json
import os

import streamlit as st
import requests
import pandas as pd
from dotenv import load_dotenv


load_dotenv()


st.set_page_config(page_title='Ask Questions about the Christian Faith')

llm_name = st.selectbox('Language model', ['mistral.mixtral-8x7b-instruct-v0:1'])
max_tokens = st.number_input('max_tokens', 4096)
temperature = st.number_input('temperature', min_value=0.0, max_value=10.0, value=0.7)
top_p = st.number_input('top_p', min_value=0.0, max_value=1.0, value=0.8)

question = st.text_area('Your Question')

if st.button('Ask!'):
    payload = json.dumps({
        'question': question,
        'llm_name': llm_name,
        'llm_config': {
            'max_tokens': max_tokens,
            'temperature': temperature,
            'top_p': top_p
        }
    })

    url = os.getenv('APIURL')
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    result_dict = json.loads(response.text)

    st.write(result_dict['answer'])

    sources = [{
        'source': os.path.basename(item['metadata']['source']),
        'page': item['metadata']['page'],
        'page_content': item['page_content']
    } for item in result_dict['source_documents']]
    st.dataframe(pd.DataFrame.from_records(sources))
