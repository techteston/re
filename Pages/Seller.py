import streamlit as st
import pandas as pd
from io import StringIO

st.set_page_config(
    page_title="Seller Portal",
    page_icon="",
)

hide_st_style = """"
<style>
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style,unsafe_allow_html=True)

st.title("Welcome to the Seller Portal")
df = pd.DataFrame()
uploaded_file = st.file_uploader("Choose a file",type=['csv','xlsx'])
if uploaded_file is not None:
    print("File Uploaded Successfully")
    try:
        df=pd.read_csv(uploaded_file)
    except:
#        print(e)
        df_invt=pd.read_excel(uploaded_file,sheet_name="Inventory")
        df_fcst=pd.read_excel(uploaded_file,sheet_name="Forecast")
        df_incm=pd.read_excel(uploaded_file,sheet_name="Incoming")
        st.caption("Current Inventory")
        df_invt
        st.caption("Current Forecast by Week")
        df_fcst
        st.caption("Incoming Deliveries")
        df_incm

