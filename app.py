import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

st.title('Dæk Danmarks energibehov')

with st.sidebar:
    solpaneler_km2 = st.slider('Solpaneler km2', 0, 200, 0)  # min: 0h, max: 23h, default: 17h
    vindmøller_km2 = st.slider('Vindmøller km2', 0, 200, 0)  # min: 0h, max: 23h, default: 17h
    batterier_km2 = st.slider('Batterier km2', 0, 100, 0)  # min: 0h, max: 23h, default: 17h


col1, col2, col3 = st.columns(3)
col1.metric("Årlig Production", "0 GWh", "")
col2.metric("Årligt forbrug", "34316 GWh", "")
col3.metric("Dækning", "0%", "")


df = pd.DataFrame(
   np.random.randn(1000, 2) / [50, 50] + [55.76, 12.4],
   columns=['lat', 'lon'])

st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=55.76,
        longitude=11.8,
        zoom=6,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
           'HexagonLayer',
           data=df,
           get_position='[lon, lat]',
           radius=2000,
           elevation_scale=4,
           elevation_range=[0, 1000],
           pickable=True,
           extruded=True,
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=df,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=200,
        ),
    ],
))
