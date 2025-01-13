import streamlit as st
from AiDataAnalyzer.data_fetch import exl_to_csv, read_data, lst_to_strng, data_for_duckdb, output_makeup
from AiDataAnalyzer.text_generator import sql_query_chain, final_answer_chain
import duckdb as db
import pandas as pd


# streamlit page configuration
st.set_page_config(
  page_title="Ai Data Analyzer",
  page_icon="💭",
  layout="centered"
)

  
st.title('AI Data Analyzer')

if "chat_history" not in st.session_state:
  st.session_state.chat_history = []
  
if "df" not in st.session_state:
  st.session_state.df = None

uploaded_file = st.file_uploader("Upload your file:",type=['csv','xlsx','xls'])

if uploaded_file:
  st.session_state.df = read_data(uploaded_file)
  
  column_list, column_names = lst_to_strng(st.session_state.df)
  
  temp_file_duckdb = data_for_duckdb(column_list=column_list,df=st.session_state.df)
  
  DATA_BASE = db.read_csv(temp_file_duckdb)
  db_name = "DATA_BASE"
  
  st.write("Data Preview")
  agree = st.checkbox("Show the Whole Data")
  if agree:
    st.dataframe(st.session_state.df)
  else:
    st.dataframe(st.session_state.df.head())
    
for message in st.session_state.chat_history:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])
    
user_question = st.chat_input("Ask anything about the Data")

if user_question:
  st.chat_message("User").markdown(user_question)
  st.session_state.chat_history.append({"role":"User","content":user_question})
  
  sql_chain = sql_query_chain()
  
  result = sql_chain.invoke({"columns":column_names,"db":db_name,"user_question":user_question})
  
  op_strng = output_makeup(result)
  print(result)
  ans = db.sql(op_strng).to_df()
  ans_dict = ans.to_dict(orient='list')
  
  ans_chain = final_answer_chain()
  
  final_result = ans_chain.invoke({"user_question":user_question,"answer":ans_dict})
  
  
  st.session_state.chat_history.append({"role":"assistant","content":(final_result)})
  
  with st.chat_message("assistant"):
    st.markdown(final_result)
    st.text("Use the query to fetch the data from your DataBase:")
    st.code(op_strng, language="sql",line_numbers=False, wrap_lines=True)