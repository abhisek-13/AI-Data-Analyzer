import pandas as pd
import tempfile


def exl_to_csv(filepath):
  df = pd.read_excel(filepath)
  with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_csv_file:
    df.to_csv(temp_csv_file.name,index=False)
  temp_file_path = temp_csv_file.name
  return temp_file_path

def read_data(filepath):
  if filepath.name.endswith(".csv"):
    df = pd.read_csv(filepath)
  elif filepath.name.endswith(".xlsx"):
    temp_filepath = exl_to_csv(filepath=filepath)
    df = pd.read_csv(temp_filepath)
  else:
    temp_filepath = exl_to_csv(filepath=filepath)
    df = pd.read_csv(temp_filepath)
    
  return df

def lst_to_strng(df):
  column_names = df.columns.tolist()
  upr_lst = []

  for i in column_names:
    upr_lst.append(i.replace(" ", "").replace("(", "").replace(")", "").upper())

  strng = ", ".join([i.replace(" ", "").replace("(", "").replace(")", "").upper() for i in column_names])

  return upr_lst, strng

def data_for_duckdb(column_list,df):
  df.columns = column_list


  with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_csv_file:
      # Save the DataFrame to the temporary CSV file
      df.to_csv(temp_csv_file.name, index=False)

      # Get the path of the temporary file
      temp_csv_file_path = temp_csv_file.name
  return temp_csv_file_path

def output_makeup(text):
  text = text.replace("\n"," ")
  text = text.replace("\t"," ")
  text = text.replace("("," ")
  text = text.replace(")"," ")
  text = text.replace("sql","")
  text = text.replace("```", "").strip()
  return text
  
  
   