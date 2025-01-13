import os
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

os.environ['NVIDIA_API_KEY'] = "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"

llm = ChatNVIDIA(model="meta/llama-3.3-70b-instruct")

def sql_query_chain():
  sql_query_prompt_template = ChatPromptTemplate.from_template(
    template="""
  You are an expert in SQL. Given a list of columns from a database table and a question from the user, generate a valid SQL query to retrieve the required information. Ensure the query is precise, uses appropriate SQL syntax, and includes necessary conditions or filters based on the user's question.

  List of columns: {columns}

  Table name: {db}

  User question: {user_question}

  Provide the SQL query below:
  Don't change the column names, use the columns as usual what ever given.
  Strictly give only the SQL query, not other fancy things or information.
  """)
  chain = sql_query_prompt_template | llm | StrOutputParser()
  return chain


def final_answer_chain():
  qna_template = ChatPromptTemplate.from_template(
    template="""Read the question and answer and form a sentence and give as output.

  Question: {user_question}

  Answer: {answer}

  Strictly give only the answer of the particular question in a single or double line sentence, don't give any fancy things.""")
  
  chain = qna_template | llm | StrOutputParser()
  return chain

