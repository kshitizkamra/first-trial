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


db_settlement['order_line_id'] = db_settlement['order_line_id'].astype(str) 
db_settlement['return_id'] = db_settlement['return_id'].astype(str)
db_settlement['order_release_id'] = db_settlement['order_release_id'].astype(str)
db_settlement['Packet_Id'] = db_settlement['Packet_Id'].astype(str)
db_settlement['MRP']=db_settlement['MRP'].astype(str)

db_settlement=db_settlement.drop(['Payment_Type'],axis=1)
i=0
db_settlement.fillna('0',inplace=True)


db_settlement=db_settlement.groupby(['NEFT_Ref','NOD_Comment','Store_Order_id','order_line_id','seller_order_id','return_id','Order_Type','order_release_id','Packet_Id','Seller_Id','comments','MRP']).agg({'igst_amount':'sum','cgst_amount':'sum','sgst_amount':'sum','customer_paid_amt':'sum','Commission':'sum','IGST_TCS':'sum','CGST_TCS':'sum','SGST_TCS':'sum','TDS':'sum','total_logistics_deduction':'sum','pick_and_pack_fee':'sum','fixed_fee':'sum','Payment_Gateway_Fee':'sum','Logistics_Commission':'sum','Settled_Amount':'sum','taxable_amount':'sum','Tax_Rate':'sum','seller_discount':'sum','platform_discount':'sum','total_discount':'sum','rvsAdditionalCharges':'sum','techEnablement':'sum','airLogistics':'sum','royaltyCharges':'sum','royaltyPercent':'sum','marketingCharges':'sum','marketingPercent':'sum','marketingContribution':'sum','Payment_Date':'max'})
st.write(db_settlement.shape)
st.write(db_settlement)
