import streamlit as st
import pandas as pd
import numpy as np
import sys
import glob
import os
from sqlalchemy import create_engine

import time


conn = st.connection("my_database")
db_master=conn.query("select * from style_master;")
db_sales=conn.query("select * from total_sales;")
db_settlement=conn.query("select * from settlement;")


db_sales_1=pd.DataFrame()
db_sales_1 = db_sales.merge(
  db_settlement,
  left_on=['sale_order_code'],
  right_on=['order_release_id']
)
db_sales_final = db_sales_1.merge(
  db_master,
  left_on=['sku_code'],
  right_on=['sku code']
)


st.write(db_sales_1)

db_analysis=pd.DataFrame(columns=['van','myntra_style_id','customer_paid_amount','total_payment_received','total_order_count','successful_order_count','asp','unit_paid_amount','cost','p/l','return %','roi','total_profit'])
db_analysis['van']=db_master['van']
db_analysis['myntra_style_id']=db_master['style id']
db_analysis['cost']=db_master['cogs_1']

db_analysis=db_analysis.drop_duplicates()
db_analysis = db_analysis.set_index('van')
db_analysis.fillna(0,inplace=True)



order_count=0
latest_iteration = st.empty()
bar = st.progress(0)
i=0
bar_progress_records=len(db_sales_final)


for index,rows in db_sales_final.iterrows():
    
    db_analysis.loc[rows.van,'total_payment_received']=db_analysis.loc[rows.van,'total_payment_received']+rows.settled_amount
    if rows.order_type=='Forward' :
        db_analysis.loc[rows.van,'customer_paid_amount']=db_analysis.loc[rows.van,'customer_paid_amount']+rows.customer_paid_amt  
        db_analysis.loc[rows.van,'total_order_count']=db_analysis.loc[rows.van,'total_order_count']+1
        db_analysis.loc[rows.van,'successful_order_count']=db_analysis.loc[rows.van,'successful_order_count']+1
    else :
        db_analysis.loc[rows.van,'successful_order_count']=db_analysis.loc[rows.van,'successful_order_count']-1

    latest_iteration.text(f'first itteration {i/bar_progress_records*100} %')
    bar.progress(i/bar_progress_records)
    i=i+1


        
db_analysis['asp']=db_analysis['customer_paid_amount']/db_analysis['total_order_count']
count=0

for index,rows in db_analysis.iterrows():
    if rows.successful_order_count==0:
        db_analysis.loc[index,'unit_paid_amount']=rows.total_payment_received
    
        
    else :
        db_analysis.loc[index,'unit_paid_amount']=db_analysis.loc[index,'total_payment_received']/db_analysis.loc[index,'successful_order_count']
    

db_analysis['p/l']=db_analysis['unit_paid_amount']-db_analysis['cost']
db_analysis['return %']=(db_analysis['total_order_count']-db_analysis['successful_order_count'])/db_analysis['total_order_count']
db_analysis['roi']=db_analysis['p/l']/db_analysis['cost']
db_analysis['total_profit']=db_analysis['p/l']*db_analysis['successful_order_count']

    
db_analysis=db_analysis[db_analysis.total_order_count!=0]

db_analysis['return %'] = db_analysis['return %'].map('{:.2%}'.format)
db_analysis['roi'] = db_analysis['roi'].map('{:.2%}'.format)


st.write(db_analysis)

orders=db_analysis['total_order_count'].sum()
suc_order=db_analysis['successful_order_count'].sum()
cust_paid=db_analysis['customer_paid_amount'].sum()
pay_rcvd= db_analysis['total_payment_received'].sum()
asp=cust_paid/orders
unit_paid_amt=pay_rcvd/suc_order
cogs=db_analysis['cost'].mean()
pl=unit_paid_amt-cogs
ret=(orders-suc_order)/orders
roi=pl/cogs
total_profit=pl*suc_order

st.write("total orders = " + str(orders))

st.write("successful orders = " + str(suc_order))
st.write("customer paid amount = " + str(cust_paid))
st.write("payment received = " + str(pay_rcvd))
st.write("asp = " + str(asp))
st.write("unit_paid_amount = " + str(unit_paid_amt))
st.write("COGS = " + str(cogs))
st.write("P/L = " + str(pl))
st.write("Return % = " + str(ret *100)+"%")
st.write("ROI % = " + str(roi*100)+"%")
st.write("Total Profit = " + str(total_profit))

         
