import streamlit as st
import plotly.graph_objects as go

hide_st_style = """
<style>
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style,unsafe_allow_html=True)

st.title("Welcome to the Buyer Portal")

def create_nodes(fd_data,fv_value_name,fv_value,fv_location,fv_color):
    nodes_trace = go.Scattermapbox(
        lat=fd_data['Latitude'],
        lon=fd_data['Longitude'],
        mode='markers',
        marker=dict(
            size=fd_data[fv_value]/50,
            color=fv_color,  # Circle color
            opacity=0.7,
        ),
        text=fv_value_name+" at " + fd_data[fv_location] + ": " + fd_data[fv_value].astype(str),
    )
    return(nodes_trace)

st.caption("Locate and Bid on products available for Sale")
if 'key' in st.session_state:
    df_available = st.session_state['key']
    df_available2 = df_available[df_available["WoS Threshold"] < df_available["Weeks of Supply"]]
    df_available2
    df_buyer_nodes = create_nodes(df_available2,"Inventory","Inventory","Location","Green")
        # Create the map layout
    layout = go.Layout(
        mapbox=dict(
            center=dict(lat=df_available2['Latitude'].mean(), lon=df_available2['Longitude'].mean()),
            zoom=3,
            style='open-street-map',
        ),
        showlegend=False,
    )


    # Create the figure
    fig = go.Figure(data=[df_buyer_nodes], layout=layout)

    # Streamlit app
    st.subheader('Currently Available Products')
    st.caption("The following products are available for Purchase")
    fig.update_layout(height=600)
    st.plotly_chart(fig,height=600)
