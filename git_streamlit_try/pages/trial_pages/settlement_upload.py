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
path = r'C:/Users/kshit/streamlit_vb/settlement/' # use your path
all_files = glob.glob(os.path.join(path , "*.csv"))

bar_progress_files=len(all_files)

db_settlement = pd.DataFrame()

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    db_settlement = pd.concat([db_settlement, df], ignore_index=True, sort=False)
    latest_iteration.text(f'Iteration {i/bar_progress_files*100} %')
    bar.progress(i/bar_progress_files)
    i=i+1


db_settlement.columns = [x.lower() for x in db_settlement.columns]




engine = create_engine('postgresql://90northbrands:90northbrands@localhost:5432/myntra_roi')

db_settlement.to_sql(
    name="final_settlement", # table name
    con=engine,  # engine
    if_exists="replace", #  If the table already exists, append
    index=False # no index
)

    







