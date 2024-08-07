import streamlit as st
import pandas as pd
import numpy as np
import sys
import glob
import os
from sqlalchemy import create_engine

import time


latest_iteration = st.empty()
bar = st.progress(0)
i=0
path = r'C:/Users/kshit/streamlit_vb/sales/' # use your path
all_files = glob.glob(os.path.join(path , "*.csv"))

bar_progress_files=len(all_files)

db_sales = pd.DataFrame()

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    db_sales = pd.concat([db_sales, df], ignore_index=True, sort=False)
    latest_iteration.text(f'Iteration {i/bar_progress_files*100} %')
    bar.progress(i/bar_progress_files)
    i=i+1

i=0
print(db_sales.shape)
db_sales=db_sales.drop_duplicates()

st.write("merged now")


db_sales['year'] = db_sales['Order_Created_Date'].str[:4]
db_sales['month'] = db_sales['Order_Created_Date'].str[5]+db_sales['Order_Created_Date'].str[6]
db_sales['date'] = db_sales['Order_Created_Date'].str[8]+db_sales['Order_Created_Date'].str[9]


db_sales.columns = [x.lower() for x in db_sales.columns]


conn = st.connection("my_database")

df_sales_original=conn.query("select * from style_sales;")

db_sales=pd.concat([db_sales,df_sales_original],ignore_index=True)
db_sales=db_sales.drop_duplicates()


engine = create_engine('postgresql://90northbrands:90northbrands@localhost:5432/myntra_roi')

db_sales.to_sql(
    name="total_sales", # table name
    con=engine,  # engine
    if_exists="replace", #  If the table already exists, append
    index=False # no index
)





