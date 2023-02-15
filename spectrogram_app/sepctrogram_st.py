import streamlit as st
import pandas as pd
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import RendererAgg
_lock = RendererAgg.lock

# Define a function to calculate and plot the spectrogram
def plot_spectrogram(df, window, noverlap, nfft):
    f, t, Sxx = signal.spectrogram(df.values, window, noverlap=noverlap, nfft=nfft)
    plt.pcolormesh(t, f, np.log10(Sxx))
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')

# Create a Streamlit app
st.title('Time-Series Spectrogram')

# Upload a CSV file with the time-series data
file = st.file_uploader('Upload a CSV file with the time-series data:', type=['csv'])

if file is not None:
    # Read the CSV file into a pandas dataframe
    df = pd.read_csv(file, index_col=0)

    # Display the data and spectrogram side by side
    col1, col2 = st.beta_columns(2)
    with col1:
        st.write('Time-Series Data:')
        st.write(df)
    with col2:
        # Get the user-defined parameters for the spectrogram
        window = st.selectbox('Window', ('hamming', 'hann', 'blackman', 'bartlett', 'flattop'))
        noverlap = st.slider('Overlap', min_value=0, max_value=100, value=50, step=1)
        nfft = st.slider('NFFT', min_value=64, max_value=4096, value=256, step=64)

        # Display the spectrogram
        st.write('Spectrogram:')
        with _lock:
            fig, ax = plt.subplots()
            plot_spectrogram(df, window, noverlap, nfft)
            st.pyplot(fig)


######################################################################################################
######################################################################################################
# import streamlit as st
# import pandas as pd


# st.set_page_config(
#     page_title="Spectrogram Generator",
#     page_icon="🧊",
#     layout="wide",
#     initial_sidebar_state="expanded",
#     menu_items={
#         'Get Help': 'https://www.extremelycoolapp.com/help',
#         'Report a bug': "https://www.extremelycoolapp.com/bug",
#         'About': "# This is a header. This is an *extremely* cool app!"
#     }
# )

# df = pd.read_csv(r"C:\Users\hanus\Desktop\root\my_github\timeseries\spectrogram_app\input_file.csv")

# st.title('Spectrogram Generator')

# print("reached here! phew!")

# list(df.columns)



