import os.path
from PIL import Image
import streamlit as st
from magnet import config as c
from magnet.constants import material_names, material_manufacturers, excitations_download
from magnet.io import load_metadata

STREAMLIT_ROOT = os.path.dirname(__file__)


def ui_download_data(m, streamlit_root):

    if m == 'A':
        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Voltage and current data from the oscilloscope ')
            st.write("""
                This .zip file contains a .txt file with information regarding the setup and core under test and several .csv files.
                   
                The .csv files contain the information for the current and for the voltage, this is, the samples measured from the oscilloscope.
                Each row is a different measurement (i.e. a data point with a different frequency, flux density, etc.)
                and each column is a sample; there are 2.000 samples per data-point.
                The sampling time is 10 ns, so the total waveform last 20 us.
                
                Additionally, the commanded duty cycles and frequency of each data point are included in separated .csv files.
                Each row correspond to the same row in the voltage and current files.
            """)
        with col2:
            st.subheader('Single switching cycle post-processed B-H data')
            st.write("""
                   This .zip file contains 4 files.
    
                   A .txt file with information regarding the setup, core under test, and post-processing information.
    
                   A .cvs file for the B waveform, where each row is a data point, and each column is a sample.
                   100 samples are saved per data point.
    
                   A .csv file for the H waveform, with the same structure as the B file.
    
                   Finally, a .csv file contains the information of the sampling time, where each row corresponds to the data-point of the B and H files.
               """)
        col1, col2 = st.columns(2)
        with col1:
            st.image(Image.open(os.path.join(STREAMLIT_ROOT, 'img', 'download_raw.png')), width=500)
        with col2:
            st.image(Image.open(os.path.join(STREAMLIT_ROOT, 'img', 'download_single.png')), width=500)

    st.sidebar.header(f'Information: Case {m}')
    excitation = st.sidebar.selectbox(
        f'Excitation:',
        excitations_download,
        key=f'excitation {m}')
    material = st.sidebar.selectbox(
        f'Material:',
        material_names,
        key=f'material {m}')
    if excitation == "Sinusoidal":
        read_excitation = 'Sinusoidal'
    if excitation == "Triangular":
        read_excitation = 'Trapezoidal'
    if excitation == "Trapezoidal":
        read_excitation = 'Trapezoidal'

    st.title(f'Download Data: Case {m}')
    st.subheader(f'{material_manufacturers[material]} - {material}, '
                 f'{excitation} excitation')

    metadata = load_metadata(material, read_excitation)
    with st.expander("Measurement details"):
        if read_excitation == 'Sinusoidal':
            st.write(metadata['info_date_sine'])
        if read_excitation == 'Trapezoidal':
            st.write(metadata['info_date_trap'])
        st.write(metadata['info_excitation'])
        st.write(metadata['info_core'])
        if read_excitation == 'Sinusoidal':
            st.write(metadata['info_setup_sine'])
        if read_excitation == 'Trapezoidal':
            st.write(metadata['info_setup_trap'])
        st.write(metadata['info_scope'])
        st.write(metadata['info_volt_meas'])
        st.write(metadata['info_curr_meas'])

    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Voltage and current data from the oscilloscope ')
        if os.path.isfile(os.path.join(
                streamlit_root, c.streamlit.raw_data_file.format(material=material, excitation=excitation))):

            data_file_raw = os.path.join(
                streamlit_root,
                c.streamlit.raw_data_file.format(material=material, excitation=excitation))
            with open(data_file_raw, 'rb') as file:
                st.download_button(f'Download zip file', file, os.path.basename(data_file_raw), key=[m, 'Raw'])
        else:
            st.write('Download data missing, please contact us')

    with col2:
        st.subheader('Single switching cycle post-processed B-H data')
        if os.path.isfile(os.path.join(
                streamlit_root, c.streamlit.single_cycle_file.format(material=material, excitation=excitation))):
            data_file_cycle = os.path.join(
                streamlit_root, c.streamlit.single_cycle_file.format(material=material, excitation=excitation))
            with open(data_file_cycle, 'rb') as file:
                st.download_button(f'Download zip file', file, os.path.basename(data_file_cycle), key=[m, 'Cycle'])
        else:
            st.write('Download data missing, please contact us')

    st.sidebar.markdown("""---""")
    st.markdown("""---""")
