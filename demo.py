from AiDataAnalyzer.data_fetch import exl_to_csv, read_data, lst_to_strng, data_for_duckdb, output_makeup
from AiDataAnalyzer.text_generator import sql_query_chain, final_answer_chain
import duckdb as db


def main():
  df = read_data('training_and_development_data.csv')
  
  column_list, column_names = lst_to_strng(df)
  
  temp_file_duckdb = data_for_duckdb(column_list=column_list,df=df)
  
  DATA_BASE = db.read_csv(temp_file_duckdb)
  
  db_name = "DATA_BASE"
  
  user_question = "How many employees are failed or incomplete the training in training outcome."
  
  sql_chain = sql_query_chain()
  
  result = sql_chain.invoke({"columns":column_names,"db":db_name,"user_question":user_question})
  
  op_strng = output_makeup(result)
  
  ans = db.sql(op_strng).to_df()
  ans_dict = ans.to_dict(orient='list')
  
  ans_chain = final_answer_chain()
  
  final_result = ans_chain.invoke({"user_question":user_question,"answer":ans_dict})
  
  print(final_result)
  
if __name__ == "__main__":
  main()
  
  