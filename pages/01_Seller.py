import streamlit as st
import pandas as pd

hide_st_style = """
<style>
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style,unsafe_allow_html=True)

def get_lat_lon(fd_data,fv_location):

    data_locations = [
    {"Location": "London", "Latitude": 51.5074, "Longitude": -0.1278},
    {"Location": "Birmingham", "Latitude": 52.4813, "Longitude": -1.9038},
    {"Location": "Leeds", "Latitude": 53.7972, "Longitude": -1.5477},
    {"Location": "Sheffield", "Latitude": 53.3806, "Longitude": -1.4750},
    {"Location": "Bradford", "Latitude": 53.7958, "Longitude": -1.7543},
    {"Location": "Liverpool", "Latitude": 53.4098, "Longitude": -2.9703},
    {"Location": "Bristol", "Latitude": 51.4511, "Longitude": -2.5893},
    {"Location": "Manchester", "Latitude": 53.4348, "Longitude": -2.2379},
    {"Location": "Edinburgh", "Latitude": 55.9523, "Longitude": -3.1880},
    {"Location": "Glasgow", "Latitude": 55.8626, "Longitude": -4.2677}
    ]
    
    df_data_locations = pd.DataFrame(data_locations)
    
    df_lat_long = pd.merge(fd_data,df_data_locations,left_on=fv_location,right_on="Location",how="left")
    
    return(df_lat_long)


st.title("Welcome to the Seller Portal")
st.caption("Determine potential slow moving Products and mark for Sale")

df = pd.DataFrame()
uploaded_file = st.file_uploader("Upload an Excel File",type=['csv','xlsx'])
if uploaded_file is not None:
    st.success('File Uploaded Successfully!', icon="✅")
#    st.balloons()
    try:
        df=pd.read_csv(uploaded_file)
    except:
#        print(e)
        df=pd.read_excel(uploaded_file,sheet_name="Inventory")
        df_invt=pd.read_excel(uploaded_file,sheet_name="Inventory")
        df_fcst=pd.read_excel(uploaded_file,sheet_name="Forecast")
        df_incm=pd.read_excel(uploaded_file,sheet_name="Incoming")
        with st.expander("Uploaded Data", expanded=False):
            st.caption("Current Inventory") 
            df_invt
            st.caption("Current Forecast by Week")
            df_fcst
            st.caption("Incoming Deliveries")
            df_incm
if len(df) > 0:
    with st.expander('Current Weeks of Supply', expanded=False):
        df_invt2 = df_invt.copy()
        df_fcst2 = df_fcst.melt(id_vars=['Product'])
        df_fcst2.rename(columns={"variable":"Week","value":"Forecast"},inplace=True)
        df_incm2 = df_incm.melt(id_vars=['Product'])
        df_incm2.rename(columns={"variable":"Week","value":"Incoming"},inplace=True)
        # Construct a Dataframe with the full weeks (pick first or minmum week and max week or last week) 
        # The products must be a combination of the products in inventory, forecast and incoming.
        df_fcst_inc = pd.merge(df_fcst2,df_incm2,on=["Product","Week"],how="left")
        df_invt2["Week"] = df_fcst_inc["Week"].iloc[0]
        df_fcst_inc_inv = pd.merge(df_fcst_inc,df_invt2,on=["Product","Week"],how="left")
        df_fcst_inc_inv.fillna(0,inplace=True)
        li_products = pd.unique(df_fcst_inc_inv["Product"])
        li_products = li_products.tolist()

        df_psi_all = pd.DataFrame(columns=['Product', 'Week', 'Forecast', 'Incoming','Inventory','ending_inventory','N4WK Forecast Average','Weeks of Supply'])

        ctr = 0

        while ctr < len(li_products):
            print(li_products[ctr])
            df_psi = df_fcst_inc_inv[df_fcst_inc_inv["Product"] == li_products[ctr]].reset_index(drop=True)
            df_psi.sort_values(by='Week', inplace=True)
            df_psi['ending_inventory'] = 0
            df_psi.at[0, 'ending_inventory'] = df_psi.at[0, 'Inventory'] + df_psi.at[0, 'Incoming'] - df_psi.at[0, 'Forecast']
            for i in range(1, len(df_psi)):
                df_psi.at[i, 'ending_inventory'] = df_psi.at[i-1, 'ending_inventory'] + df_psi.at[i, 'Incoming'] - df_psi.at[i, 'Forecast']
            df_psi["N4WK Forecast Average"] = df_psi['Forecast'].shift(-1) + df_psi['Forecast'].shift(-2) + df_psi['Forecast'].shift(-3) + df_psi['Forecast'].shift(-4)
        # Using the following to remove the Nan
            # df_psi4["N4WK Forecast"] = df_psi4['Forecast'].rolling(window=2, min_periods=1).mean()    
            df_psi["Weeks of Supply"] = df_psi['ending_inventory'] / df_psi["N4WK Forecast Average"]
        # Use concat and not append
            #    df_psi_all = pd.concat(df_psi_all,df_psi4,ignore_index=True)
            df_psi_all = pd.concat([df_psi_all, df_psi], ignore_index=True)
            # df_psi_all = df_psi_all.append(df_psi,ignore_index=True)
            
            ctr = ctr + 1

        # How to propose in future weeks
        df_psi_all_fweek = df_psi_all[df_psi_all["Week"] == df_fcst_inc["Week"].iloc[0]].reset_index(drop=True)

        df_slow_propose = df_psi_all_fweek[["Product","Week","Weeks of Supply"]]

        df_slow_propose["WoS Threshold"] = 0
        
        df_slow_propose_edited = st.data_editor(
        df_slow_propose,
        column_config={
            "Product": "Product",
            "Week":"Week",
            "Weeks of Supply":"Weeks of Supply",
            "WoS Threshold":"WoS Threshold",
        },
        disabled=["Product", "Week","Weeks of Supply"],
        hide_index=True,
    )
        
    for key in st.session_state.keys():
        del st.session_state[key]

    if st.button('Approve for Selling'):
        st.write(len(df_slow_propose_edited))
        df_slow_determined = df_slow_propose_edited[df_slow_propose_edited["WoS Threshold"] < df_slow_propose_edited["Weeks of Supply"]]
        st.write(len(df_slow_determined))
        # Either the City Information should be carried over or its need to be merged later.
        df_slow_determined = pd.merge(df_slow_determined,df_invt,on="Product",how="left")
        if 'key' not in st.session_state:
            df_slow_locations = get_lat_lon(df_slow_determined,"Location")
            st.session_state['key'] = df_slow_locations



