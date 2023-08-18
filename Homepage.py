import streamlit as st

st.set_page_config(
    page_title="Grocery Marketplace",
    page_icon="",
)


hide_st_style = """
<style>
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style,unsafe_allow_html=True)

st.title("The Produce Marketplace")
st.subheader('A Marketplace for Grocers, Retailers and Farmers')

