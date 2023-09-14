import streamlit as st
from langchain.llms import OpenAI



st.title('⚽️ Soccer Genie')

openai_api_key = st.sidebar.text_input('OpenAI API Key')

def generate_response(input_text):
  llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
  return (llm(input_text))

with st.form('my_form'):
  text = st.text_area('Enter text:', 'Ask about this seasons premier league stats')
  submitted = st.form_submit_button('Submit')
  if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
  if submitted and openai_api_key.startswith('sk-'):
    query  = generate_response(text)

exec(query)
import io
import sys
old_stdout = sys.stdout
sys.stdout = buffer = io.StringIO()
        
try:
    exec(query, globals())
    output = buffer.getvalue()
except Exception as e:
    output = str(e)
finally:
    sys.stdout = old_stdout


    st.info(output)