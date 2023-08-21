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

st.title("The :green[Produce] Marketplace")
st.subheader('A Marketplace for Grocers, Retailers and Farmers')

choice = st.selectbox('Login/SignUp',['Log In','Sign Up'])
if choice == "Log In":
    usrid = st.text_input('User ID')
    paswd = st.text_input('Password',type='password')
    st.button('Log In')
else:
    usrid = st.text_input('User ID')
    paswd = st.text_input('Password',type='password')
    st.button('Sign Up')

st.write('Selection',choice)

