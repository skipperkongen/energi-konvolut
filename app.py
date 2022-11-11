import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

# https://www.gasel.dk/vaerd-at-vide/hvor-meget-stroem-producerer-en-vindmoelle
# https://nyheder.tv2.dk/klima/2022-08-30-her-er-de-danske-havvindmoelleeventyr

st.title('Dæk Danmarks energibehov med vedvarende kilder')

st.warning('Advarsel: Antager at solen altid skinner og vinden altid blæser. TODO: batterier', icon="⚠️")

with st.sidebar:
    sol_km2 = st.slider('Solpaneler km2', 0, 200, 0)  # min: 0h, max: 23h, default: 17h
    vind_GW = st.slider('Vindmøller GW', 0, 10, 2)  # min: 0h, max: 23h, default: 17h
    batterier_km2 = st.slider('Batterier km2', 0, 100, 0)  # min: 0h, max: 23h, default: 17h

def get_consumption():
    return 34.3

def get_km2():
    return sol_km2 + batterier_km2

def get_procent_danmark():
    area_used = sol_km2 + batterier_km2
    return 100*round(area_used/42_951.0, 2)

def get_production():
    sol_TWh = round(0.21739130434*sol_km2, 2)
    vind_TWh = vind_GW * 5333 / 1000
    return round(sol_TWh + vind_TWh, 2)


col1, col2, col3, col4 = st.columns(4)
col1.metric("Årlig production", f"{get_production()} TWh", "")
col2.metric("Årligt forbrug", f"{get_consumption()} TWh", "")
col3.metric("Dækning", f"{round(get_production()/get_consumption(), 2)*100}%", "")
col4.metric("Areal (% af Danmark)", f"{get_procent_danmark()}%", "")


def get_solar_points():
    jylland = [56.42129, 9.40491]
    df = pd.DataFrame(
       np.random.randn(200, 2) / [50, 50] + jylland,
       columns=['lat', 'lon'])
    return df.iloc[:sol_km2]

def get_wind_points():
    anholt = [56.59229, 11.33309]
    df = pd.DataFrame(
       np.random.randn(200, 2) / [50, 50] + anholt,
       columns=['lat', 'lon'])
    return df.iloc[:vind_GW]

def get_battery_points():
    kbh = [55.66452, 12.351886]
    df = pd.DataFrame(
       np.random.randn(100, 2) / [50, 50] + kbh,
       columns=['lat', 'lon'])
    return df.iloc[:batterier_km2]


df = pd.concat([
    get_solar_points(),
    get_wind_points(),
    get_battery_points()
])


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
           elevation_scale=20,
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
