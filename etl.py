from sqlalchemy import create_engine
import pandas as pd
from pandas import DataFrame # for type hinting
import email_utils 
import os
from dotenv import load_dotenv
from config import DB_HOST,DATABASE_NAME,DB_PORT,EMAIL_RECEIVER,DATA_DIRECTORY

load_dotenv(os.path.join(os.path.dirname(__file__),".env"))
db_username = os.getenv("db_username")
db_password = os.getenv("db_password")


def extract(directory:str,to:str) -> None:
    """
    performs data extraction from xlsx files
    """
    try:        
        # initialize a list that will contain dataframes corresponding to each csv file        
        df_list = []
        # loop through the files inside the directory
        for f in os.listdir(directory):
            # only get the csv files
            if f.endswith('.csv'):  
                # add the dataframe containing the data of the csv to the list of dataframes                              
                df_list.append(pd.read_csv(f))
        # create a dataframe containing the data from all the dataframes ( they must all have the same column)
        all_data_df = pd.concat(df_list)
        load(all_data_df,"football_transfers",EMAIL_RECEIVER)
    except Exception as e:
        email_utils.send_mail(to,"File Upload, Data extract error:",f"Data extarct error: File location {dir}" + str(e))
        print("Data extraction error:",str(e))
         
def load(df:DataFrame,table_name:str,to:str) -> None:
    """
    performs data loading into mysql database
    """
    try:
        rows_imported = 0
        engine = create_engine(f'mysql+mysqlconnector://{db_username}:{db_password}@{DB_HOST}:{DB_PORT}/{DATABASE_NAME}')        
        print(f"importing data from importing rows{rows_imported} to {rows_imported + len(df)} ...")
        df.to_sql(f"staging_{table_name}",cong=engine,if_exists='append',index=False)
        rows_imported += len(df)
        print("Data imported successfully")
        email_utils.send_mail(to,"File uploaded, Data loaded successfully:","Data load notification for: "+ f"stg_{table_name}")        
    except Exception as e:
        email_utils.send_email(to,"File Upload Data load error:",f"Data extract error: File location {dir}" + str(e))
        print("Data load error :"+str(e))

if __name__ == "__main__":
    df = extract(DATA_DIRECTORY,EMAIL_RECEIVER)