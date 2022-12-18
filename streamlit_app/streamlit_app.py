import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(
    page_title="Time Series Analysis App",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",)

# set title for the app
st.title("""📈 Time Series Analysis App""")
st.markdown("---")

st.sidebar.markdown("## Input")

submit_form = st.sidebar.form(key='timeseries-upload-form')

ts_file = submit_form.file_uploader("Upload a file with Time Series data", type={"csv", "txt"})
time_col = submit_form.text_input("Input time column", "Date", key="time",)
value_col = submit_form.text_input("Input value column", "Close", key="value",)

submit_button = submit_form.form_submit_button('Submit')
if submit_button:
    if ts_file is not None:
        ts_df = pd.read_csv(ts_file)
        if (time_col not in ts_df.columns) or (value_col not in ts_df.columns):
            st.error(f"{time_col} or {value_col} not found in input csv file!")
        else:
            ts_df[time_col] =  pd.to_datetime(ts_df[time_col])
            st.markdown("## Input data")
            fig = px.line(ts_df, x=time_col, y=value_col)
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)
            with st.expander("Data"):
                st.dataframe(ts_df[[time_col, value_col]], use_container_width=True)
    else:
        st.sidebar.error(f"""Upload a .csv file...""")
        st.sidebar.stop()
